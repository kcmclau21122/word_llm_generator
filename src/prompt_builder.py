"""
Prompt builder module for constructing context-rich prompts for LLM generation.
Creates effective prompts with section context, user notes, and generation guidelines.
"""

from typing import Optional
from src.document_reader import Section
from src.logger_setup import get_logger


class PromptBuilder:
    """
    Builds effective prompts for LLM text generation with context and instructions.
    """
    
    def __init__(self):
        """
        Initialize prompt builder.
        """
        self.logger = get_logger()
    
    def build_section_prompt(
        self,
        section: Section,
        user_notes: str,
        document_context: str = "",
        previous_context: str = "",
        tone: str = "professional",
        length_guideline: str = "2-3 paragraphs"
    ) -> tuple[str, str]:
        """
        Build a comprehensive prompt for section content generation.
        
        Args:
            section: Section object to generate content for
            user_notes: User-provided notes and requirements
            document_context: Overall document context
            previous_context: Context from previous sections
            tone: Desired tone (professional, casual, technical, etc.)
            length_guideline: Length guidance for generated content
            
        Returns:
            Tuple of (system_message, user_prompt)
        """
        self.logger.debug(f"Building prompt for section: {section.title}")
        
        # Build system message with role and guidelines
        system_message = self._build_system_message(tone, length_guideline)
        
        # Build user prompt with all context
        user_prompt = self._build_user_prompt(
            section=section,
            user_notes=user_notes,
            document_context=document_context,
            previous_context=previous_context
        )
        
        self.logger.debug(f"Prompt built - System: {len(system_message)} chars, User: {len(user_prompt)} chars")
        
        return system_message, user_prompt
    
    def _build_system_message(self, tone: str, length_guideline: str) -> str:
        """
        Build system message with role definition and guidelines.
        
        Args:
            tone: Desired tone
            length_guideline: Length guidance
            
        Returns:
            System message string
        """
        system_message = f"""You are an expert content writer helping to create high-quality document sections.

Your task is to generate clear, well-structured content that:
- Matches the {tone} tone requested
- Is approximately {length_guideline} in length
- Flows naturally from the provided context
- Addresses all points mentioned in the user's notes
- Uses proper grammar, spelling, and formatting
- Avoids repetition and filler content

Generate only the section content itself, without adding headers, titles, or meta-commentary."""
        
        return system_message
    
    def _build_user_prompt(
        self,
        section: Section,
        user_notes: str,
        document_context: str,
        previous_context: str
    ) -> str:
        """
        Build detailed user prompt with section information and context.
        
        Args:
            section: Section to generate content for
            user_notes: User-provided notes
            document_context: Document-level context
            previous_context: Previous sections context
            
        Returns:
            User prompt string
        """
        prompt_parts = []
        
        # Document context
        if document_context:
            prompt_parts.append(f"DOCUMENT CONTEXT:\n{document_context}\n")
        
        # Section information
        prompt_parts.append(f"SECTION TO WRITE:\nTitle: {section.title}\nLevel: {section.level}\n")
        
        # Existing content (description)
        if section.content_paragraphs:
            existing = "\n".join([p for p in section.content_paragraphs if "{{" not in p])
            if existing:
                prompt_parts.append(f"EXISTING SECTION DESCRIPTION:\n{existing}\n")
        
        # Previous sections context
        if previous_context:
            prompt_parts.append(f"PREVIOUS SECTIONS CONTEXT:\n{previous_context}\n")
        
        # User notes and requirements
        prompt_parts.append(f"USER REQUIREMENTS AND NOTES:\n{user_notes}\n")
        
        # Generation instruction
        prompt_parts.append(
            "Please generate content for this section that incorporates the above requirements "
            "and flows naturally with the document context. Write the content directly without "
            "adding section headers or labels."
        )
        
        return "\n".join(prompt_parts)
    
    def build_refinement_prompt(
        self,
        section_title: str,
        original_content: str,
        refinement_notes: str
    ) -> tuple[str, str]:
        """
        Build prompt for refining/editing existing generated content.
        
        Args:
            section_title: Title of the section
            original_content: Previously generated content
            refinement_notes: User's refinement requirements
            
        Returns:
            Tuple of (system_message, user_prompt)
        """
        self.logger.debug(f"Building refinement prompt for section: {section_title}")
        
        system_message = """You are an expert editor helping to refine and improve document content.

Your task is to revise the provided content based on specific feedback while:
- Maintaining the original structure and flow where appropriate
- Addressing all refinement requirements
- Preserving the professional tone
- Improving clarity and conciseness
- Ensuring coherent transitions

Provide only the revised content without meta-commentary."""
        
        user_prompt = f"""SECTION: {section_title}

ORIGINAL CONTENT:
{original_content}

REFINEMENT REQUIREMENTS:
{refinement_notes}

Please revise the content based on these requirements."""
        
        return system_message, user_prompt
    
    def build_summary_prompt(self, content: str, max_words: int = 50) -> tuple[str, str]:
        """
        Build prompt for generating content summary.
        
        Args:
            content: Content to summarize
            max_words: Maximum words in summary
            
        Returns:
            Tuple of (system_message, user_prompt)
        """
        system_message = "You are a skilled summarizer. Create concise, accurate summaries that capture key points."
        
        user_prompt = f"""Please provide a concise summary (maximum {max_words} words) of the following content:

{content}

Summary:"""
        
        return system_message, user_prompt
    
    def estimate_token_count(self, text: str) -> int:
        """
        Rough estimation of token count for cost/limit tracking.
        Uses simple heuristic: ~4 characters per token on average.
        
        Args:
            text: Text to estimate
            
        Returns:
            Estimated token count
        """
        return len(text) // 4