#!/usr/bin/env python3
import json, sys, argparse, subprocess, tempfile, shutil, os, csv
from pathlib import Path
from datetime import datetime
import yaml

ROOT = Path(__file__).resolve().parents[2]  # project root
META_DIR = ROOT / "ingested_data" / "meta"
SNAPSHOT = META_DIR / "opportunity.readiness.json"

def load_snapshot():
    if not SNAPSHOT.exists():
        return None
    return json.loads(SNAPSHOT.read_text())

def load_spec_content(spec_paths):
    """Load content from YAML spec files and return merged context data"""
    spec_content = {}
    
    for spec_path in spec_paths:
        spec_file = Path(spec_path)
        if not spec_file.exists():
            continue
            
        try:
            with open(spec_file, 'r') as f:
                spec_data = yaml.safe_load(f)
            
            spec_id = spec_data.get('id', 'unknown')
            spec_content[spec_id] = {}
            
            # Process each section in the spec
            for section in spec_data.get('sections', []):
                section_id = section.get('id')
                
                # Handle markdown content
                if 'output' in section:
                    md_path = ROOT / section['output']
                    if md_path.exists():
                        content = md_path.read_text(encoding='utf-8').strip()
                        spec_content[spec_id][section_id] = content
                
                # Handle table content (JSON/CSV)
                if 'table_output' in section:
                    table_path = ROOT / section['table_output']
                    if table_path.exists():
                        if table_path.suffix == '.json':
                            with open(table_path, 'r') as f:
                                table_data = json.load(f)
                            spec_content[spec_id][f"{section_id}_items"] = table_data
                        elif table_path.suffix == '.csv':
                            with open(table_path, 'r') as f:
                                reader = csv.DictReader(f)
                                table_data = list(reader)
                            spec_content[spec_id][f"{section_id}_rows"] = table_data
                            
        except Exception as e:
            print(f"Warning: Failed to load spec {spec_path}: {e}", file=sys.stderr)
            continue
    
    return spec_content

def md_section(title: str) -> str:
    return f"\n\n## {title}\n\n"

def build_proposal(snap: dict, forced: bool) -> str:
    conf = int((snap.get("confidence") or 0) * 100)
    gaps = snap.get("gaps", [])
    unresolved = [g for g in gaps if not g.get("resolved")]
    unresolved_crit = [g for g in unresolved if g.get("critical")]

    # Header
    out = []
    out.append(f"# Technical & Commercial Proposal\n")
    out.append(f"**Client:** Dubai Police  \n**Project:** Dismounted Soldier Communication Kit  \n")
    out.append(f"**Confidence:** {conf}%{' (FORCED DRAFT)' if forced and conf < 95 else ''}  \n")
    out.append(f"**Generated:** {datetime.now().isoformat(timespec='seconds')}\n")

    # Executive Summary (lightweight template)
    out.append(md_section("Executive Summary"))
    out.append(
        "This proposal covers a dismounted soldier communication kit integrating **TETRA radio**, "
        "**Samsung S23/S25** device, and **INVISIO** audio with dual PTT and in-ear protection, "
        "mounted via a **foldable mid-torso bunker kit**. It addresses operational needs for Dubai Police SWAT "
        "with ruggedization, runtime, and mission readiness.\n"
    )

    # Scope / Equipment
    equip = snap.get("detected_equipment", []) or []
    confirmed_scope = []
    for g in gaps:
        if g.get("id") == "scope_clarity" and g.get("resolved") and g.get("answer"):
            confirmed_scope.append(g["answer"])
    out.append(md_section("Scope of Supply"))
    if confirmed_scope:
        out.append("- **Confirmed scope:** " + confirmed_scope[0] + "\n")
    if equip:
        out.append("**Detected items:**\n" + "\n".join(f"- {e}" for e in equip) + "\n")
    else:
        out.append("_(No automatic detections — scope confirmed via answers.)_\n")

    # Exclusions / Assumptions
    assumptions = snap.get("assumptions", []) or []
    out.append(md_section("Exclusions"))
    # Check if exclusions were confirmed
    exclusion_confirmed = any(
        (g.get("id") in ("exclude_towers", "exclusions")) and g.get("resolved")
        for g in gaps
    ) or any(
        isinstance(a, str) and "NO towers" in a
        for a in (snap.get("assumptions") or [])
    )
    
    if exclusion_confirmed:
        out.append("- **CONFIRMED EXCLUSIONS:** NO towers, NO SC4200/4400, NO Silvus radios\n")
    else:
        out.append("- _None explicitly confirmed. If towers/SC4200/Silvus exist, they are **excluded** by default._\n")

    # GFE
    gfe_items = []
    for g in gaps:
        if g.get("id") == "gfe_clarify" and g.get("resolved") and g.get("answer"):
            # Parse GFE from answer
            answer = g["answer"]
            if "TETRA" in answer:
                gfe_items.append("TETRA radios (Government Furnished)")
            if "Samsung" in answer or "S25" in answer or "S23" in answer:
                gfe_items.append("Samsung devices (Government Furnished)")
            if not gfe_items and "No GFE" not in answer:
                gfe_items.append(answer)
    
    out.append(md_section("Government Furnished Equipment (GFE)"))
    if gfe_items:
        out += [f"- {item}\n" for item in gfe_items]
    else:
        out.append("- _No GFE declared._\n")

    # Operational Requirements (from answers if present)
    op_ans = ""
    for g in gaps:
        if g.get("id") == "operational" and g.get("resolved") and g.get("answer"):
            op_ans = g["answer"]
            break
    out.append(md_section("Operational Requirements"))
    out.append(op_ans + "\n" if op_ans else "_Pending confirmation (IP rating, runtime, MIL-STD, temperature)._ \n")

    # Competitive Landscape (if provided)
    comp_ans = ""
    for g in gaps:
        if g.get("id") == "competition" and g.get("resolved") and g.get("answer"):
            comp_ans = g["answer"]
            break
    out.append(md_section("Competitive Landscape"))
    out.append(comp_ans + "\n" if comp_ans else "_Unknown at this time._\n")

    # Timeline (from answers if present)
    timeline_ans = ""
    for g in gaps:
        if g.get("id") == "timeline" and g.get("resolved") and g.get("answer"):
            timeline_ans = g["answer"]
            break
    out.append(md_section("Delivery Timeline"))
    out.append(timeline_ans + "\n" if timeline_ans else "_Pending confirmation._\n")

    # Supplier Quotes (if any)
    quotes = snap.get("vendor_quotes", []) or []
    out.append(md_section("Supplier Quotes / Pricing Evidence"))
    if quotes:
        out.append("| Supplier | Item | Price | Currency |\n|---|---|---:|:---:|\n")
        for q in quotes:
            out.append(f"| {q.get('supplier','')} | {q.get('item','')} | {q.get('price','')} | {q.get('currency','USD')} |\n")
    else:
        out.append("_Quotes not provided. Pricing to be finalized._\n")

    # Risks & Assumptions (include unresolved gaps as assumptions if forced / <95)
    out.append(md_section("Assumptions & Risks"))
    if unresolved:
        out.append("**Assumptions derived from unresolved items:**\n")
        for g in unresolved:
            severity = "HIGH" if g.get("critical") else "MEDIUM"
            label = g.get('label', 'Unresolved')
            # Provide better assumptions based on gap type
            if g.get('id') == 'operational':
                guess = "Standard mil-spec requirements (IP67, 8-hour runtime, MIL-STD-810G)"
            elif g.get('id') == 'competition':
                guess = "Assuming standard competitive landscape with major integrators"
            elif g.get('id') == 'timeline':
                guess = "Standard 90-day delivery from PO"
            else:
                guess = "Standard configuration assumed"
            out.append(f"- [{severity}] {label} — Assumption: {guess}\n")
    
    if not unresolved:
        out.append("- None. All critical information confirmed.\n")

    # Clarification Questions (for anything unresolved or parked)
    out.append(md_section("Clarification Questions"))
    if unresolved:
        out.append("**The following information would improve proposal accuracy:**\n")
        for g in unresolved:
            q = g.get("question") or g.get("label")
            out.append(f"- {q}\n")
    else:
        out.append("- None outstanding. All requirements confirmed.\n")

    # Footer
    out.append("\n---\n")
    out.append(f"*Document generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  \n")
    out.append(f"*Confidence Level: {conf}%*  \n")
    if forced:
        out.append("*Note: This is a DRAFT generated with assumptions. Review all assumptions before submission.*\n")

    return "".join(out)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true", help="Generate even if confidence < 95%")
    p.add_argument("--out", default=None, help="Output path (default: proposals/proposal_<timestamp>.md)")
    p.add_argument("--format", choices=["md","html","pdf","docx"], default="md",
                   help="Export format (default: md). 'pdf' uses html_to_pdf_converter.js, 'docx' uses template")
    p.add_argument("--template", default=None,
                   help="Path to DOCX template (for --format docx). Defaults to templates/proposal_template.docx")
    p.add_argument("--spec", action="append", default=[],
                   help="Path to YAML spec file for content-driven generation (can be repeated)")
    args = p.parse_args()

    snap = load_snapshot()
    if not snap:
        print(json.dumps({"success": False, "error": "No readiness snapshot found. Run 'readiness analyze' first."}))
        sys.exit(0)

    conf = int((snap.get("confidence") or 0) * 100)
    if conf < 95 and not args.force:
        # Find next critical question
        gaps = snap.get("gaps", [])
        unresolved = [g for g in gaps if not g.get("resolved")]
        unresolved_crit = [g for g in unresolved if g.get("critical")]
        next_q = None
        if unresolved_crit:
            next_q = unresolved_crit[0].get("question")
        elif unresolved:
            next_q = unresolved[0].get("question")
        
        print(json.dumps({
            "success": False,
            "error": f"Confidence {conf}% < 95%. Use --force to generate a draft with assumptions.",
            "confidence": conf,
            "gaps_remaining": len(unresolved),
            "next_question": next_q
        }))
        sys.exit(0)

    # Track which template was used (for DOCX auditing)
    template_used = None
    pdf_engine = None
    
    content = build_proposal(snap, forced=(conf < 95))
    fmt = args.format
    
    # Determine output path based on format
    if args.out:
        out_path = Path(args.out)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = {"md": ".md", "html": ".html", "pdf": ".pdf", "docx": ".docx"}[fmt]
        out_path = ROOT / "proposals" / f"proposal_{timestamp}{ext}"
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    if fmt == "md":
        out_path.write_text(content, encoding="utf-8")
    
    elif fmt in ("html", "pdf"):
        # Convert markdown to HTML
        try:
            from markdown import markdown as md_to_html
            html_content = md_to_html(content, extensions=["tables", "fenced_code"])
            # Wrap in basic HTML document
            html = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Technical & Commercial Proposal - Dubai Police</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1, h2 {{ color: #2c3e50; }}
        h1 {{ border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        except ImportError:
            # Fallback if markdown library not installed
            html = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Technical & Commercial Proposal - Dubai Police</title>
    <style>
        body {{ font-family: monospace; margin: 40px; white-space: pre-wrap; }}
    </style>
</head>
<body>
{content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}
</body>
</html>"""
        
        if fmt == "html":
            out_path.write_text(html, encoding="utf-8")
        else:  # pdf
            # Track PDF engine for auditing
            pdf_engine = os.environ.get("PUPPETEER_EXECUTABLE_PATH", "Puppeteer default")
            # Write HTML to temp file and convert to PDF
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
                tmp.write(html)
                tmp_path = tmp.name
            
            cmd = ["node", str(ROOT / "html_to_pdf_converter.js"), tmp_path, str(out_path)]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as e:
                Path(tmp_path).unlink(missing_ok=True)
                print(json.dumps({
                    "success": False,
                    "error": f"PDF conversion failed: {e.stderr or e.stdout or str(e)}"
                }))
                sys.exit(1)
            finally:
                Path(tmp_path).unlink(missing_ok=True)
    
    elif fmt == "docx":
        try:
            from docxtpl import DocxTemplate
        except ImportError:
            print(json.dumps({
                "success": False,
                "error": "docxtpl not installed. Run: pip install --user --break-system-packages docxtpl"
            }))
            sys.exit(1)
        
        # Load spec-driven content if provided
        spec_content = {}
        if args.spec:
            spec_content = load_spec_content(args.spec)
        
        # Build rendering context from snapshot + derived text + spec content
        gaps = snap.get("gaps", []) or []
        unresolved = [g for g in gaps if not g.get("resolved")]
        quotes = snap.get("vendor_quotes", []) or []
        
        # Pull key answers (match your gap ids)
        def gap_ans(gid):
            for g in gaps:
                if g.get("id") == gid and g.get("resolved") and g.get("answer"):
                    return g["answer"]
            return ""
        
        # Parse GFE items
        gfe_answer = gap_ans("gfe_clarify")
        gfe_items = []
        if gfe_answer:
            if "TETRA" in gfe_answer:
                gfe_items.append("TETRA radios (Government Furnished)")
            if "Samsung" in gfe_answer or "S25" in gfe_answer or "S23" in gfe_answer:
                gfe_items.append("Samsung devices (Government Furnished)")
        
        ctx = {
            "title": "Technical & Commercial Proposal",
            "client": "Dubai Police",
            "project": "Dismounted Soldier Communication Kit",
            "confidence": conf,
            "confidence_percent": f"{conf}%",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_draft": conf < 95,
            
            # Major text sections (enhanced with spec content)
            "executive_summary": (
                spec_content.get("technical-proposal", {}).get("exec_summary") or
                "This proposal covers a dismounted soldier communication kit integrating "
                "TETRA radio, Samsung S23/S25 device, and INVISIO audio with dual PTT and "
                "in-ear protection, mounted via a foldable mid-torso bunker kit. "
                "It addresses operational needs for Dubai Police SWAT with ruggedization, "
                "runtime, and mission readiness."
            ),
            "scope_confirmed": (
                spec_content.get("technical-proposal", {}).get("scope") or
                gap_ans("scope_clarity") or 
                "Confirmed: NO towers, NO SC4200/4400, NO Silvus radios"
            ),
            "system_architecture": spec_content.get("technical-proposal", {}).get("system_arch", ""),
            "ruggedization": spec_content.get("technical-proposal", {}).get("ruggedization", ""),
            "integration_testing": spec_content.get("technical-proposal", {}).get("integration_testing", ""),
            "warranty_support": spec_content.get("technical-proposal", {}).get("support", ""),
            "assumptions_risks": spec_content.get("technical-proposal", {}).get("assumptions_risks", ""),
            "operational_requirements": gap_ans("operational") or 
                "Pending confirmation (IP rating, runtime, MIL-STD, temperature).",
            "competitive_landscape": gap_ans("competition") or "Unknown at this time.",
            "delivery_timeline": (
                spec_content.get("technical-proposal", {}).get("delivery_timeline") or
                gap_ans("timeline") or 
                "Pending confirmation."
            ),
            "exclusions_text": (
                spec_content.get("commercial-proposal", {}).get("exclusions") or
                "NO towers, NO SC4200/4400, NO Silvus radios"
            ),
            
            # Commercial proposal sections
            "pricing_summary": spec_content.get("commercial-proposal", {}).get("pricing_summary", ""),
            "commercial_terms": spec_content.get("commercial-proposal", {}).get("terms", ""),
            "delivery_milestones": spec_content.get("commercial-proposal", {}).get("delivery_milestones", ""),
            
            # Lists for looping
            "detected_equipment": snap.get("detected_equipment") or [],
            "gfe_items": gfe_items,
            "quotes": quotes,
            
            # Table data from specs
            "bom_items": spec_content.get("technical-proposal", {}).get("bom_items", []),
            "compliance_rows": spec_content.get("technical-proposal", {}).get("compliance_rows", []),
            "boq_rows": spec_content.get("commercial-proposal", {}).get("boq_rows", []),
            
            # Assumptions list only if anything unresolved
            "assumptions": [
                {
                    "label": g.get("label", g.get("id", "Unresolved")),
                    "risk": "HIGH" if g.get("critical") else "MEDIUM",
                    "assumption": (
                        "Standard mil-spec requirements (IP67, 8-hour runtime, MIL-STD-810G)"
                        if g.get("id") == "operational" else
                        "Assuming standard competitive landscape with major integrators"
                        if g.get("id") == "competition" else
                        "Standard 90-day delivery from PO"
                        if g.get("id") == "timeline" else
                        "Standard configuration assumed"
                    )
                } for g in unresolved
            ],
            
            # Clarification questions
            "clarification_questions": [
                g.get("question") or g.get("label") 
                for g in unresolved
            ] if unresolved else [],
        }
        
        # Determine template path
        if args.template:
            tpl_path = Path(args.template)
        else:
            # Check for existing template in multiple locations
            possible_templates = [
                ROOT / "templates" / "proposal_template.docx",
                ROOT / "BEACON RED - Technical proposal - June 2024 - V3.docx",
                Path("/Users/user/Desktop/BEACON RED - Technical proposal - June 2024 - V3.docx"),
            ]
            tpl_path = None
            for p in possible_templates:
                if p.exists():
                    tpl_path = p
                    break
            
            if not tpl_path:
                # Create a basic template if none exists
                print(json.dumps({
                    "success": False,
                    "error": "No DOCX template found. Please provide a template with --template or create templates/proposal_template.docx",
                    "searched_paths": [str(p) for p in possible_templates]
                }))
                sys.exit(1)
        
        if not tpl_path.exists():
            print(json.dumps({
                "success": False,
                "error": f"DOCX template not found: {tpl_path}"
            }))
            sys.exit(1)
        
        # Track template used for auditing
        template_used = str(tpl_path)
        
        # Render
        try:
            doc = DocxTemplate(str(tpl_path))
            doc.render(ctx)
            doc.save(str(out_path))
        except Exception as e:
            print(json.dumps({
                "success": False,
                "error": f"DOCX rendering failed: {str(e)}"
            }))
            sys.exit(1)

    # Build final response with audit info
    result = {
        "success": True,
        "confidence": conf,
        "forced": conf < 95,
        "format": fmt,
        "output_file": str(out_path),
        "message": f"Proposal generated at {out_path}" + (" (DRAFT with assumptions)" if conf < 95 else "")
    }
    
    # Add audit information
    if template_used:
        result["template_used"] = template_used
    if pdf_engine and fmt == "pdf":
        result["pdf_engine"] = pdf_engine
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()