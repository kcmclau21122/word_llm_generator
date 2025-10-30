# Word LLM Generator - Setup Instructions

## Folder Structure

```
word_llm_generator/
├── src/
│   ├── __init__.py
│   ├── config_manager.py
│   ├── logger_setup.py
│   ├── document_reader.py
│   ├── llm_client.py
│   ├── prompt_builder.py
│   ├── content_inserter.py
│   └── table_calculator.py
├── logs/                    (created automatically)
├── templates/               (create manually - store your Word templates here)
├── output/                  (created automatically)
├── app.py
├── config.json
└── requirements.txt
```

## Python Virtual Environment Setup

### Step 1: Create Virtual Environment

```bash
# Navigate to project directory
cd word_llm_generator

# Create virtual environment using Python 3.13
python3.13 -m venv venv

# Or if python3.13 is your default python:
python -m venv venv
```

### Step 2: Activate Virtual Environment

**On Linux/Mac:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

### Step 1: Edit config.json

Open `config.json` and configure your LLM provider:

**For Ollama (Local or Cloud):**
```json
{
  "llm_provider": "ollama",
  "ollama": {
    "base_url": "http://localhost:11434",
    "model": "deepseek-r1:7b",
    "timeout": 120
  }
}
```

**For OpenAI:**
```json
{
  "llm_provider": "openai",
  "openai": {
    "api_key": "your-api-key-here",
    "model": "gpt-4o-mini",
    "organization": null
  }
}
```

**Note:** You can also set the OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Step 2: Verify Ollama Setup (if using Ollama)

**Local Models:**
```bash
# Check if Ollama is running
ollama list

# Pull DeepSeek model if not present
ollama pull deepseek-r1:7b
```

**Cloud Models via Ollama:**
For models like DeepSeek that aren't local but accessible through Ollama's cloud service, ensure you're using the correct model name and that Ollama can reach the cloud endpoint.

## Creating Word Templates

### Template Requirements

1. Use standard heading styles (Heading 1, Heading 2, Heading 3)
2. Insert placeholder `{{SECTION_CONTENT}}` where you want AI-generated content
3. For tables with calculations, use labels: "Total", "Difference", "Average"

### Example Template Structure

```
Heading 1: Executive Summary
{{SECTION_CONTENT}}

Heading 2: Market Analysis
Some descriptive text about what this section should cover...
{{SECTION_CONTENT}}

Heading 2: Financial Projections
{{SECTION_CONTENT}}

[Table with "Total" row for automatic calculations]
```

## Running the Application

### Start Streamlit App

```bash
# Make sure virtual environment is activated
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage Workflow

1. **Upload Template**: Click "Browse files" and select your .docx template
2. **Review Sections**: Check detected sections and placeholders
3. **Generate Content**: For each section:
   - Enter your notes and requirements
   - Select tone and length
   - Click "Generate Content"
   - Review generated content
4. **Finalize**: 
   - Choose whether to process table calculations
   - Enter output filename
   - Click "Save Final Document"
   - Download the completed document

## Logging

- Log files are created in the `logs/` directory
- Filename format: `app_YYYYMMDD_HHMMSS.log`
- Logs rotate hourly (configurable in config.json)
- Old logs (>1 day) are automatically deleted
- Check logs for detailed operation information and troubleshooting

## Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

### OpenAI API Errors
- Verify API key is correct
- Check your OpenAI account has credits
- Ensure you're using a valid model name

### Document Processing Errors
- Ensure template uses standard Word heading styles
- Verify placeholder pattern matches config.json
- Check that .docx file is not corrupted
- Review logs for detailed error messages

### Module Import Errors
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip list`
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

## Advanced Configuration

### Adjusting Generation Parameters

In `config.json`:
- `temperature`: 0.0-1.0 (lower = more deterministic, higher = more creative)
- `max_tokens`: Maximum length of generated content
- `top_p`: Nucleus sampling parameter

### Customizing Heading Styles

Add or modify heading styles in `config.json`:
```json
"document": {
  "section_heading_styles": ["Heading 1", "Heading 2", "Title", "Subtitle"]
}
```

### Changing Log Rotation

In `config.json`:
```json
"logging": {
  "level": "INFO",
  "rotation_hours": 1,
  "retention_days": 1
}
```

## Cost Estimation

**OpenAI Pricing (as of 2025):**
- GPT-4o-mini: ~$0.0025/1K input tokens, ~$0.01/1K output tokens
- Typical 5-section document: $0.50-$2.00

**Ollama:**
- Local models: Free (uses your compute)
- Cloud models: Check Ollama pricing for specific models\
