# 🚀 Generic MCP Proposal System - Quick Start Guide

**Transform any project into professional proposals in 3 commands**

This system is completely client-agnostic and works for any industry, client, or project type.

---

## 🎯 3-Command Quick Start

### **For Any New Project**

```bash
# 1. Copy & Configure Spec
cp spec/_blueprint.yaml spec/my-project.yaml
# Edit spec/my-project.yaml: replace {{PROJECT_ID}}, {{CLIENT_NAME}}, {{PROJECT_NAME}}

# 2. Scaffold Content
cp -r content/_sample content/my-project
# Auto-creates section templates with guiding prompts

# 3. Generate Professional Documents
python3 ingested_data/meta/proposal_builder.py --spec spec/my-project.yaml --format docx
# Outputs: Professional DOCX with corporate branding
```

**That's it!** You now have a professional proposal ready for client presentation.

---

## 🔧 MCP Natural Language Interface (Recommended)

Instead of command-line tools, use natural language commands:

```
help                                    # List all available commands
proposal build name:my-project format:docx  # Generate professional docs
readiness analyze                       # Check project completeness  
ingest status                          # View system health
```

### **MCP Command Examples**

```bash
# Content-First Mode (New Projects)
proposal outline new name:ai-platform client:"TechCorp" project:"AI Data Platform"
proposal content draft name:ai-platform section:exec_summary
proposal content approve name:ai-platform section:exec_summary
proposal build name:ai-platform format:docx out:outputs/techcorp-proposal.docx

# Legacy Snapshot Mode (Existing Projects)  
readiness analyze                      # Scan existing project files
readiness status                       # Check confidence score
readiness answer pricing: "Budget is $500K-750K"
generate proposal force:true          # Create draft with assumptions
```

---

## 📋 Project Structure Overview

```
MCP-Proposal-System/
├── spec/                              # Project specifications (YAML)
│   ├── _blueprint.yaml               # Generic template for any project
│   └── my-project.yaml               # Your project spec
├── content/                          # Generated content (per project)  
│   ├── _sample/                      # Generic content templates
│   └── my-project/                   # Your project content
├── templates/                        # Corporate templates (DOCX)
│   ├── proposal_template.docx        # Your corporate template
│   └── README.md                     # Template instructions
├── outputs/                          # Generated documents
│   └── my-project-proposal.docx      # Professional output
├── examples/                         # Working examples
│   ├── ai-platform/                  # Complete AI platform example
│   └── tactical-systems/             # Complete tactical systems example
└── mcp-server/                       # MCP server and tools
```

---

## 🎨 Customization Guide

### **1. Corporate Template Setup**

```bash
# Add your corporate DOCX template
cp /path/to/your-template.docx templates/proposal_template.docx

# Template should include:
# - Corporate logo and branding
# - Professional headers/footers  
# - Consistent styling and fonts
# - Variable placeholders: {{CLIENT_NAME}}, {{PROJECT_NAME}}, etc.
```

### **2. Project Specification (YAML)**

```yaml
id: my-project
title: {{CLIENT_NAME}} – {{PROJECT_NAME}} Proposal
client: TechCorp
project: AI Data Platform
quantity: 5
investment_range: "$500,000 - $750,000"

sections:
  - id: exec_summary
    title: Executive Summary
    output: content/my-project/exec_summary.md
    target_words: 250
    priority: critical
```

### **3. Content Development**

Each section gets auto-scaffolded with:
- **Guiding prompts** - Questions to help you write
- **Structure templates** - Professional formatting
- **Word targets** - Optimal section length
- **Priority levels** - Critical, high, medium

---

## 📊 Export Formats

| Format | Use Case | Requirements |
|--------|----------|-------------|
| **DOCX** | Client presentations, contracts | Corporate template required |
| **PDF** | Distribution, email attachments | LibreOffice or pandoc |
| **HTML** | Web sharing, quick preview | Built-in styling |
| **MD** | Development, version control | Always available |

### **Format-Specific Commands**

```bash
# Professional DOCX (with corporate branding)
python3 ingested_data/meta/proposal_builder.py --spec spec/my-project.yaml --format docx

# Distributable PDF
python3 ingested_data/meta/proposal_builder.py --spec spec/my-project.yaml --format pdf

# Quick HTML preview
python3 ingested_data/meta/proposal_builder.py --spec spec/my-project.yaml --format html

# Development Markdown
python3 ingested_data/meta/proposal_builder.py --spec spec/my-project.yaml --format md
```

---

## 🔍 Quality Gates & Validation

### **Built-in Validation**

- **Word count targets** - Ensure sections hit optimal length
- **Content completeness** - Check for placeholder content
- **Template validation** - Verify corporate branding applied
- **Link integrity** - Validate internal references
- **Format consistency** - Ensure professional presentation

### **Confidence Scoring**

```bash
readiness analyze    # Get project confidence score
# 95%+ = Ready for client presentation
# 80%+ = Can generate draft with assumptions  
# <80% = Needs more information
```

---

## 🚀 Advanced Features

### **Multi-Project Management**

```bash
# Generate multiple projects simultaneously
for project in ai-platform tactical-comms infrastructure; do
  python3 ingested_data/meta/proposal_builder.py --spec spec/$project.yaml --format docx
done
```

### **Batch Processing**

```bash
# Process all specs in spec/ directory
find spec/ -name "*.yaml" ! -name "_blueprint.yaml" -exec \
  python3 ingested_data/meta/proposal_builder.py --spec {} --format docx \;
```

### **CI/CD Integration**

The system includes GitHub Actions workflows for:
- **Auto-archive** - Version control for completed projects
- **Quality gates** - Automated validation
- **Release management** - Professional deliverable packaging

---

## 📁 Example Projects

**Location**: `./examples/`

Complete working examples for rapid cloning:

```
examples/
├── ai-platform/                      # AI/ML platform proposal
│   ├── spec/ai-platform.yaml        # Full specification
│   ├── content/ai-platform/         # All sections completed
│   └── outputs/                      # Generated documents
└── tactical-systems/                # Tactical communication system
    ├── spec/tactical-system.yaml    # Hardware-focused spec
    ├── content/tactical-system/     # Equipment specifications
    └── outputs/                     # Professional deliverables
```

### **Clone an Example**

```bash
# Start with AI platform example
cp examples/ai-platform/spec/ai-platform.yaml spec/my-ai-project.yaml
cp -r examples/ai-platform/content/ai-platform content/my-ai-project

# Customize for your client
sed -i 's/EARTH/YourClient/g' spec/my-ai-project.yaml
sed -i 's/EARTH/YourClient/g' content/my-ai-project/*.md

# Generate professional documents
python3 ingested_data/meta/proposal_builder.py --spec spec/my-ai-project.yaml --format docx
```

---

## 🔧 System Health & Maintenance

### **Health Checks**

```bash
ping                 # MCP server health
ingest status        # Data pipeline health  
readiness analyze    # Content validation
```

### **Troubleshooting**

```bash
# Fix common issues
chmod +x verify_system.sh && ./verify_system.sh

# Reset if needed
rm -rf outputs/* && rm -rf ingested_data/meta/session.*

# Rebuild MCP server
cd mcp-server && npm install && npm run build
```

---

## 💡 Best Practices

### **Project Organization**

1. **Use descriptive IDs**: `ai-platform-v2` not `project1`
2. **Version your specs**: Keep old versions for reference
3. **Separate by client**: One spec per client engagement
4. **Archive completed projects**: Move to `examples/` when done

### **Content Writing**

1. **Start with executive summary**: This sells the entire proposal
2. **Use guiding prompts**: They ensure nothing is missed
3. **Hit word targets**: Optimal length for executive attention
4. **Review before generating**: Polish content before DOCX export

### **Quality Assurance**

1. **Test with sample data**: Ensure templates work correctly
2. **Review generated docs**: Check formatting and branding
3. **Validate client-specific content**: Remove generic placeholders
4. **Version control everything**: Git track specs and content

---

**🎯 RESULT**: Professional, client-ready proposals generated in minutes, not days.**

*This system scales from individual consultants to enterprise teams, maintaining quality and consistency across all engagements.*