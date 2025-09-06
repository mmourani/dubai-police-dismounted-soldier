# Templates Directory

This directory contains document templates for proposal generation.

## Required Template

**proposal_template.docx** - Corporate DOCX template for professional proposals
- Must be placed in this directory for DOCX export to work
- Should include corporate branding, headers, footers, and styling
- Template variables will be replaced during document generation

## Template Requirements

The DOCX template should include:
- Corporate logo and branding
- Professional formatting and styles
- Header and footer with company information
- Table of contents placeholder
- Section numbering (1, 1.1, 1.2 format)
- Consistent fonts and spacing

## Adding Your Template

1. Place your corporate DOCX template in this directory
2. Name it `proposal_template.docx`
3. Test document generation to ensure proper variable replacement
4. Verify all corporate branding renders correctly

## Template Variables

The following variables are replaced during generation:
- {{CLIENT_NAME}} - Client organization name
- {{PROJECT_NAME}} - Project title
- {{INVESTMENT_RANGE}} - Budget range
- {{PROJECT_ID}} - Unique project identifier
- {{TODAY}} - Current date

## Fallback Behavior

If no template is provided:
- Markdown export will work normally
- HTML export will work normally  
- PDF export will work with basic styling
- DOCX export will fail with clear error message

**Status**: Template required for full functionality