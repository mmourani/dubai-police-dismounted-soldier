# MCP Proposal Workspace — User Guide (Generic)

## 1. Concepts
- **Spec (YAML)**: Defines sections, word targets, tables, and outputs.
- **Content (MD/CSV/JSON)**: Approved text + data the exporter assembles.
- **Templates (DOCX)**: Your corporate formatting, no pandoc reshaping.
- **MCP Tools**: Natural-language commands to ingest, draft, assemble, release.

## 2. End-to-end flow
1. **Ingest**: `ingest plan` → `ingest status` → `ingest refresh` → `ingest apply dry:false`
2. **Outline**: `proposal outline new ...` → `proposal outline approve`
3. **Draft**: `proposal draft critical/high/medium` (iterate as needed)
4. **Assemble/QA**: `proposal assemble all` → `proposal qa`
5. **Release**: `proposal release vX.Y` → (CI auto-archive on main)
6. **Delivery**: `proposal deliver vX.Y` (ZIP + notes + email template)

## 3. Content-first authoring
- Edit `spec/<project>.yaml` to define sections and data tables.
- Draft in `content/<project>/...` (MD/CSV/JSON).
- Keep language generic until client context is provided.

## 4. Exporting

Use `proposal assemble all`, or call Python directly:

```bash
python3 ingested_data/meta/proposal_builder.py \
  --spec spec/<project>.yaml --format docx --out outputs/<project>.docx
```

DOCX requires `templates/proposal_template.docx`.

## 5. CI/CD & Archiving
- CI enforces checks and uploads artifacts.
- Auto-archive moves non-essential root files to `archive/<VERSION>/`.
- Releases live in `releases/<project>-vX.Y/` with checksums.

## 6. Troubleshooting
- **DOCX fails**: add/verify `templates/proposal_template.docx`.
- **PDF fails**: ensure Puppeteer/Chromium present or set `PUPPETEER_EXECUTABLE_PATH`.
- **Spec errors**: validate YAML; ensure section output paths exist or are creatable.
- **Timeouts**: run drafting by priority (critical → high → medium).

## 7. Best practices
- One project per spec; keep content small and modular.
- Use CSV/JSON for tables (BOM/BOQ/Compliance/Risks).
- Keep examples in `examples/` out of the main flow.