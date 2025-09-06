# MCP Proposal Generation System

## Status

[![Proposal CI](https://github.com/user/project/actions/workflows/proposal-ci.yml/badge.svg)](https://github.com/user/project/actions/workflows/proposal-ci.yml)
![Confidence](https://img.shields.io/badge/confidence-100%25-brightgreen?style=flat&logo=checkmarx)
![Formats](https://img.shields.io/badge/export-MD%2FHTML%2FPDF%2FDOCX-blue?style=flat&logo=microsoftword)
![Audit](https://img.shields.io/badge/audit--trail-enabled-orange?style=flat&logo=lock)

## Quick Start

### Content-First Mode (NEW)
```bash
# Generate from spec + content
python3 ingested_data/meta/proposal_builder.py \
  --spec spec/my-project.yaml \
  --format docx \
  --out outputs/my-project-proposal.docx
```

### Snapshot Mode (Legacy)
```bash
npm run proposal:docx    # Generate from readiness snapshot
npm run proposal:pdf     # Generate PDF
npm run proposal:all     # Generate both formats
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

## Dual-Mode Operation

### Content-First Mode (Recommended)
Section-by-section collaborative approach:
- Create YAML specification (`spec/project.yaml`)
- Develop content in markdown files (`content/project/`)
- Populate structured data (BOM, BOQ, compliance tables)
- Generate professional documents when ready

### Snapshot Mode (Legacy)
Traditional confidence-based generation:
- Analyzes existing project documents
- Builds confidence score (0-100%)
- Generates proposals when confidence >95%
- Uses readiness snapshot for content

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

### Key Gap IDs (Snapshot Mode):
- `scope_clarity`: Equipment/solution confirmation
- `operational`: Technical requirements validation
- `competition`: Competitive landscape analysis
- `timeline`: Delivery schedule definition
- `gfe_clarify`: Government furnished equipment
- `exclusions`: Scope boundary clarification

## Template Placeholders (DOCX)

### Basic Fields
- `{{ client }}` - Client organization name
- `{{ project }}` - Project title
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
1. `templates/proposal_template.docx` (preferred)
2. `templates/your-template.docx` (custom template)
3. Default template in project root (legacy)

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
"spec" "content" "assets" "outputs" "examples"
"package.json" "package-lock.json" "requirements-proposals.txt"
"PROPOSAL_SYSTEM.md" "GET_STARTED_GENERIC.md" "README.md"
"html_to_pdf_converter.js" "node_modules" ".claude" "archive"
```

### Versioned Releases
- **Client-ready outputs**: `proposals/<project>-final/` (140MB complete packages)
- **Release snapshots**: `releases/<project>-vX.Y/` (production documents)
- **SHA256 checksums**: Written to `SHASUMS256.txt` in each release folder
- **Git tags**: Created as `release-<project>-vX.Y` for full traceability

### Example Release Workflow
```bash
# 1. Generate fresh proposals (content-first mode)
python3 ingested_data/meta/proposal_builder.py \
  --spec spec/my-project.yaml \
  --format all \
  --out outputs/my-project

# 2. Stage a new release
mkdir -p releases/my-project-v1.1
cp outputs/my-project*.* releases/my-project-v1.1/
shasum -a 256 releases/my-project-v1.1/* > "releases/my-project-v1.1/SHASUMS256.txt"

# 3. Push to main (CI auto-archives legacy content)
git add -A
git commit -m "chore(release): stage my-project-v1.1"
git push origin main

# 4. Tag the release (after CI passes)
git pull --rebase
git tag -a "release-my-project-v1.1" -m "Release v1.1"
git push origin "release-my-project-v1.1"
```

### Archive Structure
```
archive/
├── project-v1.0/                   # Version-tagged archive
│   ├── Project_Files/              # Original development files
│   ├── Datasheets/                 # Reference materials
│   ├── assets/                     # Visual assets
│   ├── logs/                       # System logs
│   └── legacy-files...             # All archived content
└── 2025-09-06_14-16-59/           # Timestamp-based archive
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

## FAQ - Generic Mode

**Q: What lives at repo root?**
A: Only essential project files: spec/, content/, templates/, outputs/, mcp-server/, and system files. Development clutter is contained in mcp-server/ or archived.

**Q: How to keep node_modules out of client zips?**  
A: Node dependencies are isolated in mcp-server/ directory. Root contains only client-deliverable content.

**Q: How to archive old runs?**
A: CI automatically archives legacy content to archive/ with version tags. Manual archiving available via npm scripts.

**Q: Can I use both content-first and snapshot modes?**
A: Yes! Content-first is recommended for new projects. Snapshot mode provides backwards compatibility.

---
*Generic MCP Proposal System*
*Multi-format export: MD, HTML, PDF, DOCX*
*Professional template integration*