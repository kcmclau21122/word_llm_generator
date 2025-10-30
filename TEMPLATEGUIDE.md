# Word Template Creation Guide

## Overview

This guide explains how to create Word templates that work perfectly with the Word LLM Generator.

## Template Anatomy

A properly structured template has three key components:

1. **Section Headings** (using Word's built-in styles)
2. **Section Descriptions** (optional context for the LLM)
3. **Content Placeholders** (where AI-generated content goes)

## Basic Template Structure

```
[Heading 1 style] Executive Summary
This section should provide a high-level overview of the entire document.
{{SECTION_CONTENT}}

[Heading 2 style] Background
Describe the context, history, and relevant background information.
{{SECTION_CONTENT}}

[Heading 2 style] Analysis
Present detailed analysis and findings.
{{SECTION_CONTENT}}

[Heading 1 style] Conclusion
Summarize key points and recommendations.
{{SECTION_CONTENT}}
```

## Step-by-Step Template Creation

### 1. Create a New Word Document

Open Microsoft Word and create a new blank document.

### 2. Add Section Headings

For each section:

1. Type your section title
2. Select the text
3. Apply a heading style:
   - **Home** tab → **Styles** group
   - Choose: Heading 1, Heading 2, or Heading 3
   - Or use keyboard shortcuts:
     - Ctrl+Alt+1 (Heading 1)
     - Ctrl+Alt+2 (Heading 2)
     - Ctrl+Alt+3 (Heading 3)

### 3. Add Descriptive Text (Optional but Recommended)

Below each heading, add 1-2 sentences describing what the section should contain. This helps the LLM understand context.

Example:
```
[Heading 2] Market Analysis
This section should analyze current market conditions, trends, and competitive landscape.
Focus on data-driven insights and quantifiable metrics.
{{SECTION_CONTENT}}
```

### 4. Add Content Placeholder

Below the description, type exactly: `{{SECTION_CONTENT}}`

⚠️ **Important**: 
- Must be exactly `{{SECTION_CONTENT}}`
- Two opening braces, two closing braces
- All uppercase
- No spaces inside the braces
- Can customize pattern in config.json if needed

### 5. Repeat for Each Section

Continue adding headings, descriptions, and placeholders for all sections.

## Advanced Template Features

### Nested Sections

You can create hierarchical structure:

```
[Heading 1] Financial Analysis
{{SECTION_CONTENT}}

  [Heading 2] Revenue Analysis
  {{SECTION_CONTENT}}

  [Heading 2] Cost Structure
  {{SECTION_CONTENT}}

  [Heading 2] Profitability
  {{SECTION_CONTENT}}

[Heading 1] Recommendations
{{SECTION_CONTENT}}
```

### Tables with Calculations

Create tables where you want automatic calculations:

```
[Heading 2] Budget Summary

Item              | Q1      | Q2      | Q3      | Q4      | Total
------------------|---------|---------|---------|---------|--------
Personnel         | $50,000 | $52,000 | $51,000 | $53,000 |
Operations        | $30,000 | $31,000 | $29,000 | $32,000 |
Marketing         | $20,000 | $22,000 | $21,000 | $23,000 |
Total             |         |         |         |         |
```

**Rules for automatic calculations:**
- Label rows/columns with: "Total", "Sum", "Difference", "Average"
- System will auto-calculate numeric values
- Preserves currency formatting

### Mixed Content

You can combine static content with generated content:

```
[Heading 1] Executive Summary

[Static paragraph that won't change]
This report was prepared for XYZ Corporation as part of the Q4 review process.

[Generated content]
{{SECTION_CONTENT}}

[More static content]
For questions, contact: analysis@example.com
```

## Template Best Practices

### ✅ DO:

1. **Use Consistent Heading Levels**
   - Heading 1 for major sections
   - Heading 2 for subsections
   - Heading 3 for detailed points

2. **Provide Context**
   - Add descriptions before placeholders
   - Explain what type of content is needed
   - Include tone/style guidance

3. **Keep Formatting Simple**
   - Use standard fonts (Calibri, Arial, Times New Roman)
   - Stick to basic formatting (bold, italic, underline)
   - Avoid complex layouts that may break

4. **Test Incrementally**
   - Start with 2-3 sections
   - Test generation
   - Add more sections once working

5. **Use Meaningful Titles**
   - Clear, descriptive section names
   - Help LLM understand content type
   - Example: "Financial Projections" vs "Section 3"

### ❌ DON'T:

1. **Don't Use Custom Styles**
   - Stick to built-in heading styles
   - Custom styles may not be detected

2. **Don't Nest Placeholders**
   - One placeholder per section
   - No placeholders inside tables

3. **Don't Over-Format**
   - Complex text boxes may cause issues
   - Avoid WordArt and fancy graphics near placeholders
   - Keep it simple for best results

4. **Don't Forget Placeholders**
   - Every section needing content must have `{{SECTION_CONTENT}}`
   - Sections without placeholders will be skipped

## Example Templates by Use Case

### Business Report Template

```
[Heading 1] Executive Summary
Provide a concise overview of key findings, recommendations, and business impact.
{{SECTION_CONTENT}}

[Heading 1] Current Situation
{{SECTION_CONTENT}}

[Heading 2] Market Conditions
{{SECTION_CONTENT}}

[Heading 2] Competitive Landscape
{{SECTION_CONTENT}}

[Heading 1] Analysis
{{SECTION_CONTENT}}

[Heading 1] Recommendations
{{SECTION_CONTENT}}

[Heading 1] Implementation Plan
{{SECTION_CONTENT}}
```

### Technical Documentation Template

```
[Heading 1] Overview
Describe the system, its purpose, and key features.
{{SECTION_CONTENT}}

[Heading 1] Architecture
{{SECTION_CONTENT}}

[Heading 2] System Components
{{SECTION_CONTENT}}

[Heading 2] Data Flow
{{SECTION_CONTENT}}

[Heading 1] API Reference
{{SECTION_CONTENT}}

[Heading 1] Deployment
{{SECTION_CONTENT}}

[Heading 2] Requirements
{{SECTION_CONTENT}}

[Heading 2] Installation Steps
{{SECTION_CONTENT}}
```

### Research Paper Template

```
[Heading 1] Abstract
Summarize the research question, methodology, key findings, and implications.
{{SECTION_CONTENT}}

[Heading 1] Introduction
{{SECTION_CONTENT}}

[Heading 2] Background
{{SECTION_CONTENT}}

[Heading 2] Research Question
{{SECTION_CONTENT}}

[Heading 1] Methodology
{{SECTION_CONTENT}}

[Heading 1] Results
{{SECTION_CONTENT}}

[Heading 1] Discussion
{{SECTION_CONTENT}}

[Heading 1] Conclusion
{{SECTION_CONTENT}}
```

## Customizing Placeholder Pattern

If you prefer a different placeholder format, edit `config.json`:

```json
"document": {
  "placeholder_pattern": "{{SECTION_CONTENT}}"
}
```

Options:
- `{{SECTION_CONTENT}}`
- `[GENERATE]`
- `<INSERT_CONTENT>`
- `{AI_CONTENT}`

Just ensure it's unique and won't appear in regular text.

## Troubleshooting Templates

### "No placeholders found" Error

**Problem**: System can't find `{{SECTION_CONTENT}}`

**Solutions**:
1. Check spelling exactly: `{{SECTION_CONTENT}}`
2. Ensure no extra spaces: `{{ SECTION_CONTENT }}` ❌
3. Verify all uppercase: `{{section_content}}` ❌
4. Check it's plain text, not in text box or shape

### Sections Not Detected

**Problem**: System doesn't recognize your headings

**Solutions**:
1. Verify you used Word's built-in heading styles
2. Check Home → Styles → ensure "Heading 1/2/3" is applied
3. Confirm styles match config.json settings
4. Look at status bar: should show "Heading 1" etc.

### Formatting Lost After Generation

**Problem**: Generated content doesn't match template style

**Solutions**:
1. Keep original formatting simple
2. Use basic fonts and styles only
3. Avoid complex layouts near placeholders
4. Accept that some formatting may be simplified

## Tips for Better Results

### 1. Write Good Section Descriptions

**Poor**: "Analysis section"

**Better**: "This section should analyze market trends using recent data, highlight key findings, and explain implications for strategy."

### 2. Guide the Tone

Add tone guidance in descriptions:

"Write in a professional, data-driven tone suitable for executive leadership."

### 3. Specify Length

"Provide 2-3 detailed paragraphs covering..."

### 4. Include Examples

"For example, discuss customer segments, pricing strategies, and competitive positioning."

### 5. Request Structure

"Start with an overview, then detail three key points, and conclude with implications."

## Saving and Organizing Templates

### Recommended Structure

```
templates/
├── business_report.docx
├── technical_spec.docx
├── research_paper.docx
├── project_proposal.docx
└── meeting_minutes.docx
```

### Template Naming

Use descriptive names:
- ✅ `quarterly_financial_report_template.docx`
- ✅ `project_proposal_engineering.docx`
- ❌ `template1.docx`
- ❌ `doc.docx`

## Next Steps

1. Create your first template using this guide
2. Keep it simple: 2-3 sections to start
3. Test with the application
4. Refine based on results
5. Build your template library

## Template Checklist

Before using a template, verify:

- [ ] Uses Word's built-in heading styles (Heading 1/2/3)
- [ ] Has `{{SECTION_CONTENT}}` placeholder after each heading
- [ ] Placeholder is spelled correctly and all uppercase
- [ ] Section descriptions provide clear guidance
- [ ] Formatting is simple and standard
- [ ] Tables (if any) have clear "Total"/"Difference" labels
- [ ] File saved as .docx format
- [ ] Template tested with a simple generation first

Good luck creating your templates! 🎨
