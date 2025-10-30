# Word LLM Generator - Project Overview

## Executive Summary

This application provides an automated document generation system that:
- Reads Word document templates with section placeholders
- Collects user requirements through a web interface
- Generates high-quality content using LLMs (Ollama or OpenAI)
- Automatically calculates table totals and differences
- Saves the final document with all generated content

## Architecture

### Component Breakdown

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                   │
│                         (app.py)                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│ Config       │ │ Logger      │ │ Document     │
│ Manager      │ │ Setup       │ │ Reader       │
└──────────────┘ └─────────────┘ └──────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│ LLM Client   │ │ Prompt      │ │ Content      │
│              │ │ Builder     │ │ Inserter     │
└──────────────┘ └─────────────┘ └──────────────┘
        │
        ▼
┌──────────────┐
│ Table        │
│ Calculator   │
└──────────────┘
```

### Module Descriptions

#### 1. config_manager.py
- Loads and manages configuration from config.json
- Provides type-safe access to settings
- Supports environment variable overrides
- Separates concerns for different config sections

**Key Methods:**
- `get_llm_provider()`: Returns selected LLM provider
- `get_ollama_config()`: Ollama-specific settings
- `get_openai_config()`: OpenAI-specific settings
- `get_generation_config()`: Text generation parameters

#### 2. logger_setup.py
- Implements rotating file logging with timestamp-based filenames
- Automatically cleans up old log files (>1 day)
- Creates new log files hourly to prevent size issues
- Provides both file and console output

**Key Features:**
- Format: `app_YYYYMMDD_HHMMSS.log`
- Rotation: Every hour (configurable)
- Retention: 1 day (configurable)
- Automatic cleanup on startup and rotation

#### 3. document_reader.py
- Loads Word documents using python-docx
- Extracts sections based on heading styles
- Identifies placeholders for content insertion
- Provides context from surrounding sections

**Key Classes:**
- `Section`: Dataclass representing document section
- `DocumentReader`: Main reader with extraction logic

**Key Methods:**
- `load_document()`: Load .docx file
- `extract_sections()`: Parse document structure
- `get_sections_needing_content()`: Filter sections with placeholders
- `get_section_context()`: Build contextual information

#### 4. llm_client.py
- Unified interface for Ollama and OpenAI APIs
- Handles retries with exponential backoff
- Tracks token usage and costs
- Provides connection testing

**Supported Providers:**
- Ollama: Local and cloud models
- OpenAI: GPT-4, GPT-4o, GPT-3.5-turbo, etc.

**Key Methods:**
- `generate()`: Main text generation method
- `test_connection()`: Verify LLM availability
- `_generate_ollama()`: Ollama-specific implementation
- `_generate_openai()`: OpenAI-specific implementation

#### 5. prompt_builder.py
- Constructs context-rich prompts for LLM generation
- Includes system messages with role definitions
- Incorporates document context and user requirements
- Supports refinement and summarization prompts

**Key Methods:**
- `build_section_prompt()`: Create comprehensive generation prompt
- `build_refinement_prompt()`: Create editing prompt
- `build_summary_prompt()`: Create summarization prompt

#### 6. content_inserter.py
- Inserts generated content into Word documents
- Replaces placeholders while preserving formatting
- Handles multi-paragraph content
- Manages document saving

**Key Methods:**
- `insert_content()`: Insert generated text at placeholder
- `_split_into_paragraphs()`: Parse content into paragraphs
- `save_document()`: Save modified document

#### 7. table_calculator.py
- Detects calculation requirements in tables
- Extracts numeric values handling currency/percentages
- Performs totals, differences, and averages
- Formats results matching original style

**Supported Operations:**
- **Total/Sum**: Adds values in row or column
- **Difference**: Subtracts subsequent values from first
- **Average**: Calculates mean of values

**Detection Patterns:**
- Row calculations: Label in first column
- Column calculations: Label in last row

#### 8. app.py (Streamlit UI)
- Web-based user interface
- File upload and document analysis
- Section-by-section content generation
- Real-time preview and editing
- Final document assembly and download

**Key Functions:**
- `initialize_app()`: Setup configuration and logging
- `initialize_components()`: Create processing instances
- `sidebar_configuration()`: Render settings panel
- `main_interface()`: Main UI flow
- `process_sections()`: Content generation interface
- `finalize_document()`: Assembly and save logic

## Data Flow

1. **Initialization**
   ```
   Load config.json → Setup logging → Initialize components
   ```

2. **Document Upload**
   ```
   Upload .docx → Load document → Extract sections → Identify placeholders
   ```

3. **Content Generation** (per section)
   ```
   User notes → Build context → Create prompt → Call LLM → Store result
   ```

4. **Finalization**
   ```
   Insert all content → Process tables → Save document → Provide download
   ```

## Configuration Options

### config.json Structure

```json
{
  "llm_provider": "ollama|openai",
  "ollama": {
    "base_url": "http://localhost:11434",
    "model": "deepseek-r1:7b",
    "timeout": 120
  },
  "openai": {
    "api_key": "sk-...",
    "model": "gpt-4o-mini",
    "organization": null
  },
  "generation": {
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 0.9
  },
  "document": {
    "section_heading_styles": ["Heading 1", "Heading 2", "Heading 3"],
    "placeholder_pattern": "{{SECTION_CONTENT}}"
  },
  "logging": {
    "level": "INFO",
    "rotation_hours": 1,
    "retention_days": 1
  }
}
```

## Error Handling

### LLM Client
- Automatic retry with exponential backoff (max 3 attempts)
- Logs all API errors with full details
- Graceful degradation for connection failures

### Document Processing
- Validates file existence before loading
- Handles malformed documents gracefully
- Reports missing placeholders clearly

### Logging
- All errors logged with stack traces
- Warnings for non-critical issues
- Info level for operation tracking
- Debug level for detailed troubleshooting

## Performance Considerations

### LLM API Calls
- Sequential processing (one section at a time)
- Configurable timeout for long-running requests
- Token estimation for cost tracking

### Document Operations
- In-memory document manipulation (fast)
- Single save operation at end (efficient)
- Minimal formatting operations (preserves speed)

### Table Calculations
- O(n*m) complexity for n rows, m columns
- Regex compilation cached for efficiency
- Numeric extraction optimized with single-pass parsing

## Security Considerations

### API Keys
- Stored in config.json (add to .gitignore)
- Can use environment variables instead
- Never logged or exposed in UI

### File Operations
- Temporary files cleaned up after use
- Output directory isolated from system
- No arbitrary file system access

### Input Validation
- File type checking on upload
- Path validation for output
- Numeric validation for calculations

## Extensibility

### Adding New LLM Providers

1. Add provider config section to config.json
2. Implement `_generate_<provider>()` method in LLMClient
3. Update provider initialization logic

### Custom Calculation Types

1. Add detection pattern to TableCalculator
2. Implement calculation logic
3. Update `_perform_calculation()` method

### Additional Document Formats

1. Add format detection to DocumentReader
2. Implement format-specific parsing
3. Update ContentInserter for format-specific insertion

## Known Limitations

1. **Format Preservation**: Complex formatting may be lost during content insertion
2. **Form Fields**: Cannot create Word form fields (use placeholders instead)
3. **Sequential Processing**: Sections processed one at a time (not parallel)
4. **Table Detection**: Assumes standard table structure for calculations
5. **Large Documents**: Very large documents (1000+ pages) may have performance issues

## Future Enhancements

### Potential Improvements
- Parallel section processing for faster generation
- Advanced formatting preservation using XML manipulation
- PDF output option
- Batch processing for multiple documents
- Template library with pre-built templates
- Content versioning and revision history
- Integration with document management systems
- Support for Google Docs format

## Maintenance

### Regular Tasks
- Monitor log files for errors
- Update model configurations as new models release
- Review and optimize prompts based on output quality
- Clean output directory periodically
- Update dependencies: `pip install -r requirements.txt --upgrade`

### Troubleshooting Checklist
1. Check log files in `logs/` directory
2. Verify LLM provider is accessible (test connection button)
3. Ensure template has correct placeholder format
4. Validate document uses standard heading styles
5. Confirm adequate disk space for output files
6. Review recent config.json changes

## Support Resources

### Log Analysis
```bash
# View latest log
tail -f logs/app_*.log

# Search for errors
grep ERROR logs/app_*.log

# Count warnings
grep -c WARNING logs/app_*.log
```

### Configuration Testing
```bash
# Validate JSON syntax
python -m json.tool config.json

# Test Ollama connection
curl http://localhost:11434/api/tags

# Test OpenAI connection (requires API key)
python -c "from openai import OpenAI; OpenAI(api_key='sk-...').models.list()"
```

### Performance Profiling
```python
# Add to app.py for timing analysis
import time
start = time.time()
# ... operation ...
print(f"Operation took {time.time() - start:.2f} seconds")
```

## License & Credits

This application uses the following open-source libraries:
- python-docx: MIT License
- Streamlit: Apache License 2.0
- OpenAI Python: MIT License
- Requests: Apache License 2.0

## Version History

**v1.0.0 (Current)**
- Initial release
- Support for Ollama and OpenAI
- Template-based document generation
- Table calculations
- Rotating log files with cleanup
- Web-based Streamlit interface