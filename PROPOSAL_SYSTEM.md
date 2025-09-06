# Dubai Police Proposal Generation System

## Status

[![Proposal CI](https://github.com/mmourani/dubai-police-dismounted-soldier/actions/workflows/proposal-ci.yml/badge.svg)](https://github.com/mmourani/dubai-police-dismounted-soldier/actions/workflows/proposal-ci.yml)
![Confidence](https://img.shields.io/badge/confidence-100%25-brightgreen?style=flat&logo=checkmarx)
![Formats](https://img.shields.io/badge/export-MD%2FHTML%2FPDF%2FDOCX-blue?style=flat&logo=microsoftword)
![Audit](https://img.shields.io/badge/audit--trail-enabled-orange?style=flat&logo=lock)

## Quick Start

### Generate Proposals
```bash
npm run proposal:docx    # Generate Word document (uses BEACON RED template)
npm run proposal:pdf     # Generate PDF
npm run proposal:all     # Generate both DOCX and PDF
```

### Check Readiness
```bash
npm run readiness:check     # View current confidence level
npm run readiness:analyze   # Re-analyze all documents
```

### MCP Server
```bash
npm run mcp:build        # Rebuild TypeScript
npm run mcp:run          # Start MCP server
npm run mcp:test:docx    # Test DOCX generation via MCP
```

## System Overview

### Components
1. **Readiness Analyzer** (`ingested_data/meta/readiness_analyzer.py`)
   - Analyzes project documents
   - Tracks confidence (0-100%)
   - Identifies gaps and questions
   - Blocks proposal at <95% unless forced

2. **Proposal Builder** (`ingested_data/meta/proposal_builder.py`)
   - Generates proposals in 4 formats: MD, HTML, PDF, DOCX
   - Uses BEACON RED template for DOCX
   - Puppeteer for PDF generation
   - Auto-includes assumptions when forced

3. **MCP Server** (`mcp-server/`)
   - JSON-RPC over stdio
   - Natural language routing
   - Tool-based architecture

### File Structure
```
.
├── ingested_data/meta/
│   ├── readiness_analyzer.py      # Confidence tracking
│   ├── proposal_builder.py        # Multi-format generation
│   └── opportunity.readiness.json # Current snapshot
├── templates/
│   └── proposal_template.docx     # BEACON RED template
├── proposals/                     # Generated outputs
├── releases/                      # Versioned snapshots
└── mcp-server/                    # MCP integration
```

## Confidence System

### 100% Required For:
- Final proposals without "DRAFT" banner
- Clean output without assumptions section

### Key Gap IDs:
- `scope_clarity`: Equipment confirmation
- `operational`: IP67, runtime, MIL-STD requirements  
- `competition`: Competitor landscape
- `timeline`: Delivery schedule
- `gfe_clarify`: Government furnished equipment
- `exclusions`: Towers/SC4200/Silvus confirmation

## Template Placeholders (DOCX)

### Basic Fields
- `{{ client }}` - Dubai Police
- `{{ project }}` - Dismounted Soldier Communication Kit
- `{{ confidence_percent }}` - e.g., "100%"
- `{{ generated_at }}` - Timestamp
- `{{ is_draft }}` - Boolean for draft mode

### Content Sections
- `{{ executive_summary }}`
- `{{ scope_confirmed }}`
- `{{ operational_requirements }}`
- `{{ competitive_landscape }}`
- `{{ delivery_timeline }}`
- `{{ exclusions_text }}`

### Lists (use in Word bullets)
```jinja
{% for item in detected_equipment %}
• {{ item }}
{% endfor %}

{% for g in gfe_items %}
• {{ g }}
{% endfor %}
```

### Conditional Sections
```jinja
{% if assumptions %}
  {% for a in assumptions %}
  • [{{ a.risk }}] {{ a.label }} — {{ a.assumption }}
  {% endfor %}
{% else %}
  None. All critical information confirmed.
{% endif %}
```

## Installation

### Python Dependencies
```bash
pip3 install --user --break-system-packages -r requirements-proposals.txt
```

### Node Dependencies
```bash
npm install
cd mcp-server && npm install
```

## Troubleshooting

### Template Not Found
Check these locations in order:
1. `templates/proposal_template.docx`
2. `BEACON RED - Technical proposal - June 2024 - V3.docx` (root)
3. `/Users/user/Desktop/BEACON RED - Technical proposal - June 2024 - V3.docx`

### PDF Generation Issues
- Requires Puppeteer: `npm install puppeteer`
- Uses `html_to_pdf_converter.js`
- Check Chrome/Chromium installation

### DOCX Rendering Errors
- Ensure template has valid Jinja2 placeholders
- Check `docxtpl` is installed
- Verify template isn't corrupted

## Production Checklist

- [x] Python dependencies frozen in `requirements-proposals.txt`
- [x] BEACON RED template copied to `templates/`
- [x] NPM scripts for all workflows
- [x] Releases folder with SHA256 checksums
- [x] 100% confidence achieved
- [x] All 4 formats tested (MD/HTML/PDF/DOCX)
- [x] MCP server integration with health checks
- [x] Git LFS for large binary files
- [x] CI/CD pipeline with GitHub Actions
- [x] Audit trail in JSON output (template_used, pdf_engine)
- [x] Artifact uploads with 14-day retention
- [x] Main branch protection (95% confidence required)

## Health Monitoring

```bash
# MCP server health check
npm run mcp:ping

# Full system test
npm run proposal:test && npm run mcp:smoke

# Audit with template path
npm run proposal:docx:audit
```

## CI/CD Pipeline

The GitHub Actions workflow (`proposal-ci.yml`) runs on every push and PR:
1. Checks out code with Git LFS
2. Installs cached dependencies
3. Builds MCP server
4. Runs readiness check
5. Tests all proposal formats
6. Uploads artifacts
7. Enforces 95% confidence on main branch
8. **Auto-archives legacy root content** (main branch only)

## Archiving & Version Control

### Auto-Archive Workflow
On every push to `main`, GitHub Actions will automatically:
- Detect the latest version folder in `releases/` (e.g., `dubai-police-swat-v1.0`)
- Archive all non-essential files/folders into `archive/<VERSION>/`
- Commit changes back with: `chore(archive): auto-archive legacy root → archive/<VERSION>`
- Preserve file history using `git mv` where possible

### Keep List (What Stays in Root)
```bash
".git" ".github" ".gitattributes" ".gitignore"
"mcp-server" "ingested_data" "proposals" "releases" "templates"
"package.json" "package-lock.json" "requirements-proposals.txt"
"PROPOSAL_SYSTEM.md" "README.md" "README_FIRST.md"
"html_to_pdf_converter.js" "node_modules" ".claude" "archive"
```

### Versioned Releases
- **Client-ready outputs**: `proposals/<project>-final/` (140MB complete packages)
- **Release snapshots**: `releases/<project>-vX.Y/` (production documents)
- **SHA256 checksums**: Written to `SHASUMS256.txt` in each release folder
- **Git tags**: Created as `release-<project>-vX.Y` for full traceability

### Example Release Workflow
```bash
# 1. Generate fresh proposals
npm run proposal:all

# 2. Stage a new release
mkdir -p releases/dubai-police-swat-v1.1
cp proposals/dubai-police-swat-final/*.pdf releases/dubai-police-swat-v1.1/
cp proposals/dubai-police-swat-final/*.docx releases/dubai-police-swat-v1.1/
shasum -a 256 releases/dubai-police-swat-v1.1/* > "releases/dubai-police-swat-v1.1/SHASUMS256.txt"

# 3. Push to main (CI auto-archives legacy content)
git add -A
git commit -m "chore(release): stage dubai-police-swat-v1.1"
git push origin main

# 4. Tag the release (after CI passes)
git pull --rebase
git tag -a "release-dubai-police-swat-v1.1" -m "Release v1.1 (CI auto-archive applied)"
git push origin "release-dubai-police-swat-v1.1"
```

### Archive Structure
```
archive/
├── dubai-police-swat-v1.0/          # Version-tagged archive
│   ├── Dubai_Police_Project/        # Original development files
│   ├── Datasheets/                  # Reference materials
│   ├── pictures/                    # Visual assets
│   ├── logs/                        # System logs
│   └── legacy-files...              # All archived content
└── 2025-09-06_14-16-59/            # Timestamp-based archive
    └── legacy-content...
```

### Benefits
- **✅ Clean Repository**: Root stays focused on production essentials
- **📦 Complete Preservation**: All legacy artifacts archived with history
- **🏷 Full Traceability**: Tagged releases + version folders + timestamps
- **🤖 Zero Manual Effort**: CI handles cleanup automatically
- **📋 Client Focus**: Only presentation-ready content visible

## Recovery Procedures

### Restore Previous Snapshot
```bash
cp releases/2025-09-05_v1.0/snapshot.json ingested_data/meta/opportunity.readiness.json
```

### Use System Chrome for PDFs
```bash
export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
npm run proposal:pdf
```

### Verify Release Integrity
```bash
cd releases/2025-09-05_v1.0
shasum -c SHASUMS256.txt
```

---
*System validated: 2025-09-05*
*Confidence: 100%*
*All exclusions confirmed: NO towers, NO SC4200/4400, NO Silvus radios*
*Template: BEACON RED Technical Proposal V3*