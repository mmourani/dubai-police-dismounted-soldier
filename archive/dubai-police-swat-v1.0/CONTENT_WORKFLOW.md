# Content-First Collaborative Workflow

## Overview

The Dubai Police Proposal System now supports a **content-first, section-by-section collaborative workflow** that allows stakeholders to co-design, review, and approve proposal content before generating professional documents.

## Key Benefits

- **🤝 Collaborative Control**: Approve outlines and sections before export
- **📝 Structured Content**: YAML specifications with markdown sections and JSON/CSV tables
- **🎯 Incremental Development**: Build and validate piece-by-piece  
- **✅ Professional Quality**: Template-driven exports with approved content
- **🔄 Full Compatibility**: Works with existing CI/CD and template systems

## Repository Structure

```
dubai-police-dismounted-soldier/
├── spec/                           # Document specifications (YAML)
│   ├── technical-proposal.yaml    # Technical proposal structure
│   └── commercial-proposal.yaml   # Commercial proposal structure
├── content/                        # Approved content sections
│   ├── technical-proposal/
│   │   ├── exec_summary.md        # Executive summary (markdown)
│   │   ├── scope.md               # Scope of supply (markdown)
│   │   ├── system_arch.md         # System architecture (markdown)
│   │   ├── bom.json               # Bill of materials (JSON)
│   │   └── compliance.csv         # Compliance matrix (CSV)
│   └── commercial-proposal/
│       ├── pricing_summary.md     # Pricing overview (markdown)
│       ├── boq.csv               # Bill of quantities (CSV)
│       └── terms.md              # Commercial terms (markdown)
├── assets/                         # Images, diagrams, charts
├── outputs/                        # Generated documents
└── releases/                       # Tagged releases
```

## Workflow Process

### 1. Outline Design & Approval
```bash
# Review and customize section specifications
nano spec/technical-proposal.yaml
nano spec/commercial-proposal.yaml
```

### 2. Section-by-Section Content Development
Create approved content in structured format:

**Markdown Sections** (for narrative content):
```bash
# Executive summary
content/technical-proposal/exec_summary.md

# Scope definition  
content/technical-proposal/scope.md

# System architecture
content/technical-proposal/system_arch.md
```

**JSON Tables** (for structured data):
```json
// content/technical-proposal/bom.json
[
  {
    "item_no": 1,
    "description": "INVISIO X7 in-ear communication system",
    "qty": 10,
    "unit": "ea",
    "manufacturer": "INVISIO",
    "part_no": "X7-001",
    "unit_price_aed": 8485,
    "extended_price_aed": 84850,
    "notes": "39dB noise reduction, tactical grade"
  }
]
```

**CSV Tables** (for tabular data):
```csv
# content/technical-proposal/compliance.csv
requirement_id,text,standard,evidence_ref,compliant,notes
R-ENV-01,Ingress protection IP67,IEC 60529,Datasheets/IP,Yes,Confirmed in readiness snapshot
```

### 3. Content-Driven Document Generation

**Single Specification**:
```bash
python3 ingested_data/meta/proposal_builder.py \
  --format docx \
  --spec spec/technical-proposal.yaml \
  --out outputs/technical-proposal.docx
```

**Multiple Specifications**:
```bash  
python3 ingested_data/meta/proposal_builder.py \
  --format docx \
  --spec spec/technical-proposal.yaml \
  --spec spec/commercial-proposal.yaml \
  --out outputs/combined-proposal.docx
```

**All Formats**:
```bash
# DOCX (template-driven)
python3 ingested_data/meta/proposal_builder.py --format docx --spec spec/technical-proposal.yaml --out outputs/technical.docx

# PDF (web-based)  
python3 ingested_data/meta/proposal_builder.py --format pdf --spec spec/technical-proposal.yaml --out outputs/technical.pdf

# HTML (for review)
python3 ingested_data/meta/proposal_builder.py --format html --spec spec/technical-proposal.yaml --out outputs/technical.html
```

## YAML Specification Format

### Document Structure
```yaml
id: technical-proposal
title: Technical Proposal
template: templates/proposal_template.docx
sections:
  - id: exec_summary
    title: Executive Summary
    output: content/technical-proposal/exec_summary.md
    target_words: 250
  - id: bom
    title: Bill of Materials
    table_output: content/technical-proposal/bom.json
```

### Section Types

**Markdown Content**:
```yaml
- id: section_id
  title: Section Title
  output: content/path/section.md
  target_words: 300
```

**JSON Tables**:
```yaml  
- id: table_id
  title: Table Title
  table_output: content/path/table.json
```

**CSV Tables**:
```yaml
- id: table_id
  title: Table Title  
  table_output: content/path/table.csv
```

## Context Mapping

The enhanced `proposal_builder.py` automatically maps structured content to DOCX template variables:

### Text Sections
- `content/technical-proposal/exec_summary.md` → `{{ executive_summary }}`
- `content/technical-proposal/scope.md` → `{{ scope_confirmed }}`
- `content/technical-proposal/system_arch.md` → `{{ system_architecture }}`
- `content/commercial-proposal/terms.md` → `{{ commercial_terms }}`

### Table Data
- `content/technical-proposal/bom.json` → `{{ bom_items }}` (array for loops)
- `content/technical-proposal/compliance.csv` → `{{ compliance_rows }}` (array for loops)
- `content/commercial-proposal/boq.csv` → `{{ boq_rows }}` (array for loops)

### Template Usage
```jinja2
<!-- DOCX template placeholders -->
{{ executive_summary }}

{% for item in bom_items %}
• {{ item.description }} - {{ item.qty }} {{ item.unit }} @ AED {{ item.unit_price_aed }}
{% endfor %}

{% for row in compliance_rows %}
• {{ row.requirement_id }}: {{ row.text }} ({{ row.compliant }})
{% endfor %}
```

## Integration with Existing System

### Backwards Compatibility
The enhanced system maintains full compatibility with existing workflows:
- **Without --spec**: Uses traditional snapshot-based generation
- **With --spec**: Merges structured content with snapshot data
- **CI/CD**: All existing GitHub Actions continue to work
- **Templates**: Same DOCX template system with enhanced context

### Quality Assurance
- **95% Confidence**: Still enforced for production documents
- **Template Validation**: DOCX rendering with error handling
- **Content Validation**: YAML/JSON/CSV format validation
- **Audit Trail**: Template and content source tracking

## Migration from Legacy System

1. **Archive Legacy Content**:
   ```bash
   # Already handled by CI auto-archive
   ls archive/2025-09-06_14-16-59/
   ```

2. **Extract Existing Content**:
   ```bash
   # Copy relevant sections from existing proposals to content/ structure
   ```

3. **Validate and Test**:
   ```bash
   # Test both old and new workflows
   python3 ingested_data/meta/proposal_builder.py --format docx --out outputs/legacy-test.docx
   python3 ingested_data/meta/proposal_builder.py --format docx --spec spec/technical-proposal.yaml --out outputs/content-test.docx
   ```

## Best Practices

### Content Development
- **Review Cycle**: Outline → Draft → Review → Approve → Export
- **Version Control**: Use git for all content changes
- **Collaboration**: Multiple stakeholders can edit different sections
- **Validation**: Test exports frequently during development

### File Organization  
- **Markdown**: For narrative content (executive summaries, scope, terms)
- **JSON**: For structured data with complex objects
- **CSV**: For simple tabular data that stakeholders can edit in spreadsheets
- **Assets**: Store diagrams and images for future template integration

### Quality Control
- **Content Approval**: Each section approved before inclusion
- **Template Consistency**: All exports use professional BEACON RED template
- **Data Validation**: JSON/CSV format validation before export
- **Export Testing**: Verify both DOCX and PDF outputs before client delivery

## Success Metrics

### Implemented Features ✅
- Content-first directory structure
- YAML specification system  
- Enhanced proposal_builder.py with --spec support
- Markdown, JSON, and CSV content integration
- Template-driven DOCX/PDF export
- Multi-specification document generation
- Full backwards compatibility

### Ready for Production ✅
- Professional quality output matches existing system
- CI/CD integration maintained
- Template rendering verified
- Content validation implemented
- Audit trail preserved

The Dubai Police Proposal System now supports both traditional snapshot-based generation and the new content-first collaborative workflow, providing maximum flexibility for different use cases and stakeholder preferences.