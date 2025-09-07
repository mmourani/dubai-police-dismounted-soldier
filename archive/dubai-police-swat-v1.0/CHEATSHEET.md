# Claude CLI Cheat Sheet (Generic MCP)

Run these inside Claude CLI, in order:

## 0) Ingest & Prep
1. `ingest plan` — show what's here
2. `ingest status` — confidence + scan counts
3. `ingest refresh` — rescan/update metadata
4. `ingest apply dry:false` — archive/clean old files

## 1) Bootstrap
5. `proposal outline new name:<project> client:"<Client>" project:"<Solution>"`
6. `proposal outline approve`

## 2) Draft
7. `proposal draft critical`
8. `proposal draft high`
9. `proposal draft medium`

## 3) Assemble & QA
10. `proposal assemble all`
11. `proposal qa`

## 4) Release
12. `proposal release vX.Y`
13. `proposal archive` (CI also auto-archives on main)

## 5) Deliver
14. `proposal deliver vX.Y`

**Tip**: Use `help` for the full list of tools/commands.