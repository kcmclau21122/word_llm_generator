# Word LLM Generator - Quick Start Guide

## What You Have

A complete, production-ready Python application for automated Word document generation using LLMs. The system supports both **Ollama** (local and cloud models like DeepSeek) and **OpenAI API**.

## Project Structure

```
word_llm_generator/
├── src/                          # Core application modules
│   ├── config_manager.py         # Configuration handling
│   ├── logger_setup.py           # Rotating logs with auto-cleanup
│   ├── document_reader.py        # Word document parsing
│   ├── llm_client.py             # Unified LLM interface (Ollama + OpenAI)
│   ├── prompt_builder.py         # Context-rich prompt construction
│   ├── content_inserter.py       # Generated content insertion
│   └── table_calculator.py       # Automatic table calculations
├── app.py                        # Streamlit web interface
├── config.json                   # Configuration file (EDIT THIS!)
├── requirements.txt              # Python dependencies
├── SETUP.md                      # Detailed setup instructions
├── ARCHITECTURE.md               # Technical documentation
└── .env.example                  # Environment variable template
```

## 5-Minute Setup

### 1. Create Virtual Environment
```bash
cd word_llm_generator
python3.13 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure LLM Provider

**Option A: Ollama (Local or Cloud)**
Edit `config.json`:
```json
{
  "llm_provider": "ollama",
  "ollama": {
    "base_url": "http://localhost:11434",
    "model": "deepseek-r1:7b"
  }
}
```

**Option B: OpenAI**
Edit `config.json`:
```json
{
  "llm_provider": "openai",
  "openai": {
    "api_key": "your-key-here",
    "model": "gpt-4o-mini"
  }
}
```

### 4. Run Application
```bash
streamlit run app.py
```

Opens browser at `http://localhost:8501`

## Using the Application

### Step 1: Create a Word Template

Create a `.docx` file with:
- Standard heading styles (Heading 1, 2, 3)
- Placeholder: `{{SECTION_CONTENT}}` where you want AI-generated content

**Example Template:**
```
Executive Summary (Heading 1)
This section should provide an overview...
{{SECTION_CONTENT}}

Background (Heading 2)
Context and history...
{{SECTION_CONTENT}}
```

### Step 2: Generate Content

1. Upload your template
2. Review detected sections
3. For each section:
   - Enter your requirements/notes
   - Select tone and length
   - Click "Generate Content"
4. Save final document

### Step 3: Download

Click "Download Generated Document" to get your completed file!

## Key Features

✅ **Dual LLM Support**: Works with Ollama (including DeepSeek) and OpenAI  
✅ **Template-Based**: Uses Word templates with placeholders  
✅ **Table Calculations**: Auto-calculates totals and differences  
✅ **Robust Logging**: Hourly rotation, auto-cleanup, detailed tracking  
✅ **Web Interface**: User-friendly Streamlit UI  
✅ **Well-Structured**: Properly factored, commented Python code  
✅ **Configurable**: Everything controlled via config.json  

## Configuration Highlights

### config.json - Important Settings

```json
{
  "llm_provider": "ollama",              // or "openai"
  
  "generation": {
    "temperature": 0.7,                  // 0.0-1.0 (creativity)
    "max_tokens": 2000                   // Length limit
  },
  
  "document": {
    "section_heading_styles": [          // Customizable
      "Heading 1", "Heading 2", "Heading 3"
    ],
    "placeholder_pattern": "{{SECTION_CONTENT}}"
  },
  
  "logging": {
    "level": "INFO",                     // DEBUG for troubleshooting
    "rotation_hours": 1,                 // New log file every hour
    "retention_days": 1                  // Delete logs > 1 day old
  }
}
```

## Logging System

### Features
- **Timestamped files**: `logs/app_20250128_143052.log`
- **Hourly rotation**: New file every hour
- **Auto-cleanup**: Removes logs older than 1 day
- **Comprehensive**: Tracks all operations, errors, API calls

### View Logs
```bash
# Latest log
tail -f logs/app_*.log

# Find errors
grep ERROR logs/*.log
```

## Ollama Configuration

### Local Models
```bash
# Check Ollama is running
ollama list

# Pull a model
ollama pull deepseek-r1:7b
```

### Cloud Models (DeepSeek via Ollama)
If using DeepSeek cloud through Ollama, ensure your `base_url` and `model` are configured correctly. The application handles both local and cloud Ollama endpoints.

## OpenAI Configuration

### Set API Key

**Option 1: config.json**
```json
"openai": {
  "api_key": "sk-proj-...",
  "model": "gpt-4o-mini"
}
```

**Option 2: Environment Variable**
```bash
export OPENAI_API_KEY="sk-proj-..."
```

## Table Calculations

The system automatically detects and calculates:

- **Total/Sum**: Labels like "Total", "Sum"
- **Difference**: Labels like "Difference", "Delta"
- **Average**: Labels like "Average", "Mean"

**Example:**
```
Item        | Amount
------------|--------
Product A   | $100
Product B   | $200
Total       | $300  ← Automatically calculated
```

## Code Quality

✅ **Properly Factored**: Modular design with clear separation of concerns  
✅ **Comprehensive Comments**: Every function and class documented  
✅ **Type Hints**: Modern Python typing throughout  
✅ **Error Handling**: Robust exception handling with logging  
✅ **Best Practices**: Follows PEP 8 and Python conventions  

## Troubleshooting

### "Connection failed" error
- **Ollama**: Check `ollama serve` is running
- **OpenAI**: Verify API key is correct

### "No placeholders found"
- Ensure template uses `{{SECTION_CONTENT}}` exactly
- Check heading styles match config.json settings

### Generation fails
- Check log files in `logs/` directory
- Verify LLM model is available
- Test connection using UI button

### Import errors
- Ensure venv is activated
- Reinstall: `pip install -r requirements.txt --force-reinstall`

## Next Steps

1. **Read SETUP.md** for detailed installation instructions
2. **Read ARCHITECTURE.md** for technical deep-dive
3. **Create templates/** folder and add your Word templates
4. **Customize config.json** for your needs
5. **Run and test** with a simple template first

## Cost Considerations

### OpenAI
- **GPT-4o-mini**: ~$0.0025/1K input, ~$0.01/1K output
- **Typical document**: $0.50-$2.00 for 5 sections

### Ollama
- **Local models**: Free (uses your compute)
- **Cloud models**: Check Ollama pricing

## Support

For issues:
1. Check `logs/` directory for error details
2. Review SETUP.md troubleshooting section
3. Verify configuration in config.json
4. Test LLM connection using UI button

## What Makes This Implementation Special

1. **Dual LLM Support**: Seamlessly switch between Ollama and OpenAI
2. **Production-Ready Logging**: Proper rotation and cleanup
3. **Clean Architecture**: Well-factored, maintainable code
4. **User-Friendly**: Streamlit UI requires no technical knowledge
5. **Robust Error Handling**: Comprehensive logging and retry logic
6. **Configurable**: Everything controlled via config file
7. **Table Intelligence**: Automatic calculations without formulas

Enjoy your new document generation system! 🚀
