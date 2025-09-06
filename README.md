# MCP Proposal Generation Workspace (Generic)

A content-first, client-agnostic proposal system that works in any project folder. It lets you ingest existing materials, collaboratively draft sections, assemble professional documents (MD/HTML/PDF/DOCX), and release versioned packages — all via Claude MCP tools.

## Why this exists
- Generic-first: works for ANY client/industry without code edits
- Content-first: approve outlines & sections before exporting
- Professional outputs: DOCX/PDF via your corporate templates
- Clean repo: auto-archiving of old content and release tagging

## 3-Command Quick Start (any project)
```bash
export PROJECT_ID=my-project
export CLIENT_NAME="My Client"
export PROJECT_NAME="My Solution"

# bootstrap from blueprint
cp spec/_blueprint.yaml spec/$PROJECT_ID.yaml
sed -i.bak "s/{{PROJECT_ID}}/$PROJECT_ID/g; s/{{CLIENT_NAME}}/$CLIENT_NAME/g; s/{{PROJECT_NAME}}/$PROJECT_NAME/g" spec/$PROJECT_ID.yaml
cp -r content/_sample content/$PROJECT_ID
```

## Claude CLI workflow (plain English)

See `CHEATSHEET.md` for the one-screen command list.  
See `docs/USER_GUIDE.md` for deeper explanations & troubleshooting.

## Folder layout

```
spec/            # YAML specs (outlines, word targets, data tables)
content/         # Markdown sections + CSV/JSON tables (approved text)
templates/       # Corporate DOCX template(s)
assets/          # Images/diagrams (optional)
outputs/         # Generated proposal files (MD/HTML/PDF/DOCX)
releases/        # Versioned, checksummed packages
archive/         # Auto-archived legacy materials (via CI)
examples/        # Optional references (kept out of main flow)
mcp-server/      # MCP tools (isolated dev deps)
```

## Building documents (CLI examples)

```bash
# MD
python3 ingested_data/meta/proposal_builder.py \
  --spec spec/$PROJECT_ID.yaml --format md --out outputs/$PROJECT_ID.md

# DOCX (requires templates/proposal_template.docx)
python3 ingested_data/meta/proposal_builder.py \
  --spec spec/$PROJECT_ID.yaml --format docx --out outputs/$PROJECT_ID.docx

# PDF
python3 ingested_data/meta/proposal_builder.py \
  --spec spec/$PROJECT_ID.yaml --format pdf --out outputs/$PROJECT_ID.pdf
```

## CI & Releases
- CI runs quality checks and can auto-archive legacy root content.
- Releases live under `releases/<project>-vX.Y/` with `SHASUMS256.txt`.
- See `docs/USER_GUIDE.md` → Releases & Delivery.