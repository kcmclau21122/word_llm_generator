"""
Main Streamlit application for Word document generation with LLM integration.
Provides web interface for uploading templates, collecting input, and generating content.
"""

import streamlit as st
from pathlib import Path
import tempfile
import os
from typing import Dict, List

from src.config_manager import get_config
from src.logger_setup import setup_logging, get_logger
from src.document_reader import DocumentReader, Section
from src.llm_client import LLMClient
from src.prompt_builder import PromptBuilder
from src.content_inserter import ContentInserter
from src.table_calculator import TableCalculator


# Page configuration
st.set_page_config(
    page_title="Word LLM Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_app():
    """
    Initialize application configuration and logging.
    """
    if "initialized" not in st.session_state:
        # Load configuration
        try:
            config = get_config("config.json")
            st.session_state.config = config
            
            # Setup logging
            log_config = config.get_logging_config()
            setup_logging(
                log_dir="logs",
                retention_days=log_config["retention_days"],
                rotation_hours=log_config["rotation_hours"],
                level=log_config["level"]
            )
            
            logger = get_logger()
            logger.info("=" * 80)
            logger.info("Application started")
            logger.info(f"LLM Provider: {config.get_llm_provider()}")
            logger.info("=" * 80)
            
            st.session_state.initialized = True
            st.session_state.logger = logger
            
        except Exception as e:
            st.error(f"Failed to initialize application: {str(e)}")
            st.stop()


def initialize_components():
    """
    Initialize document processing components.
    """
    config = st.session_state.config
    logger = st.session_state.logger
    
    try:
        # Document configuration
        doc_config = config.get_document_config()
        
        # Initialize components
        if "document_reader" not in st.session_state:
            st.session_state.document_reader = DocumentReader(
                heading_styles=doc_config["section_heading_styles"],
                placeholder_pattern=doc_config["placeholder_pattern"]
            )
        
        if "prompt_builder" not in st.session_state:
            st.session_state.prompt_builder = PromptBuilder()
        
        if "content_inserter" not in st.session_state:
            st.session_state.content_inserter = ContentInserter(
                placeholder_pattern=doc_config["placeholder_pattern"]
            )
        
        if "table_calculator" not in st.session_state:
            st.session_state.table_calculator = TableCalculator()
        
        # Initialize LLM client
        if "llm_client" not in st.session_state:
            provider = config.get_llm_provider()
            
            if provider == "ollama":
                provider_config = config.get_ollama_config()
            elif provider == "openai":
                provider_config = config.get_openai_config()
            else:
                raise ValueError(f"Unsupported provider: {provider}")
            
            generation_config = config.get_generation_config()
            
            st.session_state.llm_client = LLMClient(
                provider=provider,
                provider_config=provider_config,
                generation_config=generation_config
            )
            
            logger.info("All components initialized successfully")
            
    except Exception as e:
        logger.error(f"Component initialization failed: {str(e)}")
        st.error(f"Failed to initialize components: {str(e)}")
        st.stop()


def sidebar_configuration():
    """
    Render sidebar with configuration options.
    """
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        config = st.session_state.config
        
        # Display current provider
        provider = config.get_llm_provider()
        st.info(f"**LLM Provider:** {provider.upper()}")
        
        if provider == "ollama":
            ollama_config = config.get_ollama_config()
            st.write(f"**Model:** {ollama_config['model']}")
            st.write(f"**URL:** {ollama_config['base_url']}")
        elif provider == "openai":
            openai_config = config.get_openai_config()
            st.write(f"**Model:** {openai_config['model']}")
        
        st.divider()
        
        # Generation parameters
        st.subheader("Generation Parameters")
        
        gen_config = config.get_generation_config()
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=float(gen_config["temperature"]),
            step=0.1,
            help="Higher values make output more random, lower more deterministic"
        )
        st.session_state.temperature = temperature
        
        max_tokens = st.number_input(
            "Max Tokens",
            min_value=100,
            max_value=4000,
            value=int(gen_config["max_tokens"]),
            step=100,
            help="Maximum length of generated content"
        )
        st.session_state.max_tokens = max_tokens
        
        st.divider()
        
        # Test connection button
        if st.button("🔌 Test LLM Connection", use_container_width=True):
            with st.spinner("Testing connection..."):
                if st.session_state.llm_client.test_connection():
                    st.success("✅ Connection successful!")
                else:
                    st.error("❌ Connection failed. Check logs.")


def main_interface():
    """
    Render main application interface.
    """
    st.title("📝 Word Document LLM Generator")
    st.markdown("Upload a Word template with placeholders and generate content using AI")
    
    logger = st.session_state.logger
    
    # File upload
    st.header("1️⃣ Upload Template")
    uploaded_file = st.file_uploader(
        "Choose a Word document template (.docx)",
        type=["docx"],
        help="Upload a Word document with section headings and {{SECTION_CONTENT}} placeholders"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        st.session_state.uploaded_path = tmp_path
        st.success(f"✅ Uploaded: {uploaded_file.name}")
        
        # Load and analyze document
        try:
            logger.info(f"Loading uploaded document: {uploaded_file.name}")
            
            doc = st.session_state.document_reader.load_document(tmp_path)
            sections = st.session_state.document_reader.extract_sections(doc)
            sections_with_placeholders = st.session_state.document_reader.get_sections_needing_content(sections)
            
            st.session_state.doc = doc
            st.session_state.sections = sections
            st.session_state.sections_with_placeholders = sections_with_placeholders
            
            # Display document info
            st.subheader("Document Analysis")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Sections", len(sections))
            col2.metric("Sections with Placeholders", len(sections_with_placeholders))
            col3.metric("Tables", len(doc.tables))
            
            if sections_with_placeholders:
                process_sections()
            else:
                st.warning("⚠️ No placeholders found. Make sure your template includes {{SECTION_CONTENT}} markers.")
                
        except Exception as e:
            logger.error(f"Failed to process document: {str(e)}")
            st.error(f"Failed to process document: {str(e)}")


def process_sections():
    """
    Process sections and collect user input for content generation.
    """
    st.header("2️⃣ Generate Section Content")
    
    sections_with_placeholders = st.session_state.sections_with_placeholders
    logger = st.session_state.logger
    
    # Initialize session state for generated content
    if "generated_content" not in st.session_state:
        st.session_state.generated_content = {}
    
    # Section selection
    section_titles = [s.title for s in sections_with_placeholders]
    
    tabs = st.tabs([f"Section {i+1}" for i in range(len(sections_with_placeholders))])
    
    for idx, (tab, section) in enumerate(zip(tabs, sections_with_placeholders)):
        with tab:
            st.subheader(f"📄 {section.title}")
            st.caption(f"Level {section.level} heading")
            
            # Display existing content
            if section.content_paragraphs:
                with st.expander("View existing section description"):
                    for para in section.content_paragraphs:
                        if "{{" not in para:
                            st.write(para)
            
            # User input
            user_notes = st.text_area(
                "Your notes and requirements for this section:",
                height=150,
                key=f"notes_{idx}",
                placeholder="Enter key points, requirements, or specific content you want included..."
            )
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                tone = st.selectbox(
                    "Tone",
                    ["professional", "casual", "technical", "academic", "friendly"],
                    key=f"tone_{idx}"
                )
            
            with col2:
                length = st.selectbox(
                    "Length",
                    ["1-2 paragraphs", "2-3 paragraphs", "3-4 paragraphs", "4-5 paragraphs"],
                    index=1,
                    key=f"length_{idx}"
                )
            
            # Generate button
            if st.button(f"✨ Generate Content", key=f"generate_{idx}", use_container_width=True):
                if not user_notes.strip():
                    st.warning("⚠️ Please provide some notes or requirements first.")
                else:
                    with st.spinner("Generating content..."):
                        try:
                            # Build context
                            previous_context = st.session_state.document_reader.get_section_context(
                                st.session_state.sections,
                                section
                            )
                            
                            # Build prompt
                            system_msg, user_prompt = st.session_state.prompt_builder.build_section_prompt(
                                section=section,
                                user_notes=user_notes,
                                previous_context=previous_context,
                                tone=tone,
                                length_guideline=length
                            )
                            
                            # Generate content
                            generated = st.session_state.llm_client.generate(
                                prompt=user_prompt,
                                system_message=system_msg,
                                temperature=st.session_state.get("temperature"),
                                max_tokens=st.session_state.get("max_tokens")
                            )
                            
                            # Store generated content
                            st.session_state.generated_content[section.title] = generated
                            
                            logger.info(f"Content generated for section: {section.title}")
                            st.success("✅ Content generated successfully!")
                            
                        except Exception as e:
                            logger.error(f"Generation failed for section {section.title}: {str(e)}")
                            st.error(f"Generation failed: {str(e)}")
            
            # Display generated content
            if section.title in st.session_state.generated_content:
                st.markdown("---")
                st.markdown("**Generated Content:**")
                content = st.session_state.generated_content[section.title]
                st.markdown(content)
                
                # Option to regenerate
                if st.button(f"🔄 Regenerate", key=f"regen_{idx}"):
                    del st.session_state.generated_content[section.title]
                    st.rerun()
    
    # Finalize document
    if st.session_state.generated_content:
        st.header("3️⃣ Finalize Document")
        
        col1, col2 = st.columns(2)
        
        with col1:
            process_tables = st.checkbox(
                "Process table calculations",
                value=True,
                help="Automatically calculate totals and differences in tables"
            )
        
        with col2:
            output_name = st.text_input(
                "Output filename",
                value="generated_document.docx"
            )
        
        if st.button("💾 Save Final Document", type="primary", use_container_width=True):
            with st.spinner("Creating final document..."):
                try:
                    finalize_document(process_tables, output_name)
                except Exception as e:
                    logger.error(f"Failed to finalize document: {str(e)}")
                    st.error(f"Failed to save document: {str(e)}")


def finalize_document(process_tables: bool, output_name: str):
    """
    Insert all generated content and save final document.
    
    Args:
        process_tables: Whether to process table calculations
        output_name: Output filename
    """
    logger = st.session_state.logger
    doc = st.session_state.doc
    sections_with_placeholders = st.session_state.sections_with_placeholders
    
    logger.info("Finalizing document...")
    
    # Insert generated content
    insertion_count = 0
    for section in sections_with_placeholders:
        if section.title in st.session_state.generated_content:
            content = st.session_state.generated_content[section.title]
            success = st.session_state.content_inserter.insert_content(
                doc, section, content, preserve_placeholder=False
            )
            if success:
                insertion_count += 1
    
    logger.info(f"Inserted content for {insertion_count} section(s)")
    
    # Process tables if requested
    if process_tables and doc.tables:
        calc_count = st.session_state.table_calculator.process_all_tables(doc)
        logger.info(f"Performed {calc_count} table calculation(s)")
    
    # Save document
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / output_name
    
    success = st.session_state.content_inserter.save_document(doc, str(output_path))
    
    if success:
        # Provide download button
        with open(output_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Generated Document",
                data=f,
                file_name=output_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        
        st.success(f"✅ Document saved successfully!")
        logger.info(f"Document saved: {output_path}")
        
        # Display summary
        st.balloons()
        st.markdown("### 🎉 Generation Complete!")
        col1, col2 = st.columns(2)
        col1.metric("Sections Generated", insertion_count)
        if process_tables:
            col2.metric("Table Calculations", calc_count)
    else:
        st.error("Failed to save document. Check logs for details.")


def main():
    """
    Main application entry point.
    """
    # Initialize app
    initialize_app()
    initialize_components()
    
    # Render UI
    sidebar_configuration()
    main_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Word LLM Generator v1.0 | Powered by AI"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()