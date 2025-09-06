# Content Directory

This directory contains all proposal content organized by project ID.

## Structure

```
content/
├── _sample/                    # Template content for new projects
│   ├── exec_summary.md        # Executive summary template
│   ├── scope_of_work.md       # Scope template  
│   ├── delivery_timeline.md   # Timeline template
│   ├── bom.json              # Bill of Materials sample
│   ├── boq.csv               # Bill of Quantities sample
│   ├── compliance.csv        # Compliance matrix sample
│   └── risk_register.csv     # Risk register sample
└── your-project-id/          # Your project content
    ├── exec_summary.md       # Your executive summary
    ├── scope_of_work.md      # Your scope definition
    └── ...                   # Other sections as defined in spec
```

## Starting a New Project

1. **Copy sample content**:
   ```bash
   cp -r content/_sample content/your-project-id
   ```

2. **Customize placeholders**:
   - Replace `{{CLIENT_NAME}}` with your client name
   - Replace `{{PROJECT_NAME}}` with your project name
   - Update content to match your specific requirements

3. **Follow the spec**:
   - Your `spec/your-project-id.yaml` defines which content files are required
   - File paths in the spec must match your actual content files
   - Section IDs in spec correspond to content file names

## Content Development Tips

### Markdown Files
- Use the guiding prompts (comments) to structure your content
- Remove prompts when content is finalized
- Follow target word counts specified in your spec
- Use standard markdown formatting for professional output

### Data Files (JSON/CSV)
- Follow the schema defined in your spec exactly
- Use consistent formatting and data types
- Validate JSON syntax before building documents
- Keep CSV headers matching the schema requirements

## Priority Workflow

Work through sections in priority order as defined in your spec:

1. **Critical**: exec_summary, scope_of_work, bom, boq
2. **High**: system_architecture, equipment_specifications, compliance_matrix  
3. **Medium**: delivery_timeline, risk_register, training_support

## Quality Checks

Before document generation:
- [ ] All critical and high priority sections completed
- [ ] Data files validate against schema
- [ ] Target word counts approximately met
- [ ] Client-specific requirements addressed
- [ ] Technical accuracy verified

## Integration with MCP Tools

Content files integrate automatically with:
- **proposal_builder.py**: Renders content into professional documents
- **ingest tools**: Analyze content completeness and confidence
- **quality gates**: Validate content before document generation