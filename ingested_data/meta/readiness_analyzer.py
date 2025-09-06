#!/usr/bin/env python3
"""
Readiness Analyzer for Dubai Police Project
Analyzes existing files, identifies gaps, asks only what's needed to reach 95% confidence
No assumptions, no fixed forms, just intelligent gap detection
"""

import json
import yaml
import re
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

@dataclass
class Gap:
    """Represents a knowledge gap that needs filling"""
    id: str
    label: str
    rationale: str          # Why this matters
    question: str           # The specific question to ask
    critical: bool          # If True, blocks proposal generation
    weight: float           # Impact on confidence (0.0 to 1.0)
    answer: Optional[str] = None
    resolved: bool = False
    
    def resolve(self, answer: str):
        """Mark gap as resolved with answer"""
        self.answer = answer.strip()
        self.resolved = bool(self.answer)

@dataclass
class ReadinessSnapshot:
    """Current state of opportunity readiness"""
    timestamp: str
    project_root: str
    
    # What we found
    files_scanned: int = 0
    markdown_files: List[str] = field(default_factory=list)
    pdf_files: List[str] = field(default_factory=list)
    csv_files: List[str] = field(default_factory=list)
    
    # What we detected
    detected_context: List[str] = field(default_factory=list)
    detected_equipment: List[str] = field(default_factory=list)
    detected_suppliers: List[str] = field(default_factory=list)
    detected_pricing: List[str] = field(default_factory=list)
    detected_exclusions: List[str] = field(default_factory=list)
    
    # Structured findings
    assumptions: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    gfe_items: List[str] = field(default_factory=list)
    vendor_quotes: List[Dict] = field(default_factory=list)
    
    # Competition
    competitors: List[str] = field(default_factory=list)
    win_themes: List[str] = field(default_factory=list)
    
    # Gaps and confidence
    gaps: List[Gap] = field(default_factory=list)
    confidence: float = 0.0
    suggested_next: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['gaps'] = [asdict(g) for g in self.gaps]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ReadinessSnapshot':
        """Create from dictionary"""
        gaps_data = data.pop('gaps', [])
        snapshot = cls(**data)
        snapshot.gaps = [Gap(**g) for g in gaps_data]
        return snapshot

class ReadinessAnalyzer:
    """Analyzes opportunity readiness by scanning files and identifying gaps"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.meta_dir = self.project_root / "ingested_data" / "meta"
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        self.snapshot_file = self.meta_dir / "opportunity.readiness.json"
        
        # Detection patterns (domain-specific but not assumptive)
        self.patterns = {
            'radio': [r'\bTETRA\b', r'\bP25\b', r'\bDMR\b', r'\bradio\b'],
            'device': [r'\bSamsung\s+S2[35]\b', r'\bS2[35]\b', r'\bGalaxy\b'],
            'audio': [r'\bINVISIO\b', r'\bPTT\b', r'\bdual[\s-]?PTT\b', r'\bearplug'],
            'mount': [r'\bbunker\b', r'\btorso\b', r'\bfoldable\b', r'\bmount\b'],
            'excluded': [r'\btower\b', r'\bSC4[24]00\b', r'\bSilvus\b'],
            'pricing': [r'(?:USD|AED|\$)\s*[\d,]+(?:\.\d{2})?', r'\d+\s*(?:USD|AED)'],
            'supplier': [r'\bquote\b', r'\bPO\b', r'\bRFQ\b', r'\bproposal\b'],
            'gfe': [r'\bGFE\b', r'\bgovernment[\s-]?furnished\b', r'\bcustomer[\s-]?provided\b']
        }
    
    def analyze_opportunity(self) -> ReadinessSnapshot:
        """Perform initial analysis of the opportunity"""
        snapshot = ReadinessSnapshot(
            timestamp=datetime.now().isoformat(),
            project_root=str(self.project_root)
        )
        
        # Step 1: Scan files
        self._scan_files(snapshot)
        
        # Step 2: Detect context from content
        self._detect_context(snapshot)
        
        # Step 3: Identify gaps based on what we found/didn't find
        self._identify_gaps(snapshot)
        
        # Step 4: Calculate initial confidence
        self._calculate_confidence(snapshot)
        
        # Save snapshot
        self._save_snapshot(snapshot)
        
        return snapshot
    
    def _scan_files(self, snapshot: ReadinessSnapshot):
        """Scan project directory for relevant files"""
        for path in self.project_root.rglob("*"):
            if path.is_file():
                if path.suffix == ".md":
                    snapshot.markdown_files.append(str(path.relative_to(self.project_root)))
                elif path.suffix == ".pdf":
                    snapshot.pdf_files.append(str(path.relative_to(self.project_root)))
                elif path.suffix == ".csv":
                    snapshot.csv_files.append(str(path.relative_to(self.project_root)))
        
        snapshot.files_scanned = len(snapshot.markdown_files) + len(snapshot.pdf_files) + len(snapshot.csv_files)
    
    def _detect_context(self, snapshot: ReadinessSnapshot):
        """Detect context from file contents using patterns"""
        # Read up to 20 markdown files for context
        content_samples = []
        for md_file in snapshot.markdown_files[:20]:
            try:
                full_path = self.project_root / md_file
                content = full_path.read_text(errors='ignore')
                content_samples.append(content)
            except:
                pass
        
        combined_text = "\n".join(content_samples)
        
        # Detect equipment mentions
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    if category == 'radio' and 'TETRA' in pattern:
                        snapshot.detected_equipment.append("TETRA radio detected")
                    elif category == 'device' and 'S23' in combined_text:
                        snapshot.detected_equipment.append("Samsung S23 detected")
                    elif category == 'device' and 'S25' in combined_text:
                        snapshot.detected_equipment.append("Samsung S25 detected")
                    elif category == 'audio' and 'INVISIO' in pattern:
                        snapshot.detected_equipment.append("INVISIO audio detected")
                    elif category == 'mount' and 'bunker' in pattern:
                        snapshot.detected_equipment.append("Bunker mount detected")
                    elif category == 'excluded':
                        snapshot.detected_exclusions.append(f"Exclusion keyword: {pattern}")
        
        # Detect pricing
        price_matches = re.findall(self.patterns['pricing'][0], combined_text)
        if price_matches:
            snapshot.detected_pricing = price_matches[:10]  # First 10 price mentions
        
        # Detect GFE mentions
        if re.search(r'\bGFE\b', combined_text):
            snapshot.detected_context.append("GFE references found - need clarification")
        
        # Detect supplier/quote context
        if re.search(r'\bquote|supplier|vendor\b', combined_text, re.IGNORECASE):
            snapshot.detected_context.append("Supplier/vendor references found")
    
    def _identify_gaps(self, snapshot: ReadinessSnapshot):
        """Identify knowledge gaps based on what was/wasn't detected"""
        gaps = []
        
        # Gap 1: Core scope clarity - ALWAYS ASK THIS
        gaps.append(Gap(
            id="scope_clarity",
            label="Equipment scope confirmation",
            rationale="Need to confirm exact equipment included in the kit",
            question="Please confirm the complete kit scope. For Dubai Police dismounted soldier: TETRA radio + Samsung S25 + INVISIO dual PTT/earplugs + foldable torso mount. Is this correct? Any additions or changes?",
            critical=True,
            weight=0.25
        ))
        
        # Gap 2: Exclusions confirmation (critical if tower keywords detected)
        if snapshot.detected_exclusions:
            gaps.append(Gap(
                id="exclusions",
                label="Exclusions confirmation",
                rationale="Tower/SC4200/Silvus keywords detected - must confirm these are excluded",
                question="IMPORTANT: We detected tower/SC4200/Silvus references. Please confirm these are EXCLUDED from scope. Type: 'Confirmed: NO towers, NO SC4200/4400, NO Silvus radios'",
                critical=True,
                weight=0.20
            ))
        
        # Gap 3: GFE declaration
        if "GFE references found" in snapshot.detected_context:
            gaps.append(Gap(
                id="gfe_items",
                label="GFE item specification",
                rationale="GFE mentioned but not specified - critical for pricing",
                question="Which items are Government Furnished Equipment (GFE)? List each GFE item (e.g., 'TETRA radios - GFE, Samsung devices - GFE')",
                critical=True,
                weight=0.20
            ))
        elif not any("GFE" in ctx for ctx in snapshot.detected_context):
            gaps.append(Gap(
                id="gfe_clarify",
                label="GFE clarification",
                rationale="No GFE information found - need to know what customer provides",
                question="Are any items Government Furnished Equipment (customer-provided)? If yes, list them. If no, type 'No GFE items'",
                critical=True,
                weight=0.15
            ))
        
        # Gap 4: Supplier pricing (if not enough pricing detected)
        if len(snapshot.detected_pricing) < 3:
            gaps.append(Gap(
                id="supplier_quotes",
                label="Supplier pricing details",
                rationale="Limited pricing information found - need supplier quotes for accuracy",
                question="Provide key supplier quotes (format: Supplier | Item | Price | Currency | Qty). Or type 'Use standard pricing' if quotes not available",
                critical=True,
                weight=0.15
            ))
        
        # Gap 5: Operational requirements
        gaps.append(Gap(
            id="operational",
            label="Operational requirements",
            rationale="Need to understand environmental and operational constraints",
            question="What are the key operational requirements? (e.g., IP67 rating, 8-hour runtime, MIL-STD-810G, temperature range)",
            critical=False,
            weight=0.10
        ))
        
        # Gap 6: Competition (optional but valuable)
        if not snapshot.competitors:
            gaps.append(Gap(
                id="competition",
                label="Competitive landscape",
                rationale="Understanding competition improves win probability",
                question="Who are the main competitors for this opportunity? (comma-separated, or 'unknown')",
                critical=False,
                weight=0.10
            ))
        
        # Gap 7: Timeline and delivery
        gaps.append(Gap(
            id="timeline",
            label="Delivery timeline",
            rationale="Timeline affects pricing and feasibility",
            question="What is the required delivery timeline? (e.g., '90 days from PO', '6 weeks ARO')",
            critical=False,
            weight=0.05
        ))
        
        snapshot.gaps = gaps
        
        # Set suggested next question (first unresolved critical gap, then non-critical)
        critical_gaps = [g for g in gaps if g.critical and not g.resolved]
        non_critical_gaps = [g for g in gaps if not g.critical and not g.resolved]
        
        if critical_gaps:
            snapshot.suggested_next = critical_gaps[0].question
        elif non_critical_gaps:
            snapshot.suggested_next = non_critical_gaps[0].question
    
    def _calculate_confidence(self, snapshot: ReadinessSnapshot):
        """Calculate confidence score based on resolved gaps and detected context"""
        # Base confidence from file presence
        base = 0.15 if snapshot.files_scanned > 0 else 0.0
        
        # Boost from detected context (max 0.15)
        context_boost = min(0.15, len(snapshot.detected_equipment) * 0.03)
        
        # Calculate from gap resolution
        total_weight = sum(g.weight for g in snapshot.gaps)
        resolved_weight = sum(g.weight for g in snapshot.gaps if g.resolved)
        
        # Critical gap penalty
        unresolved_critical = sum(g.weight * 0.5 for g in snapshot.gaps if g.critical and not g.resolved)
        
        # Final confidence
        confidence = base + context_boost + resolved_weight - unresolved_critical
        snapshot.confidence = max(0.0, min(1.0, confidence))
    
    def _save_snapshot(self, snapshot: ReadinessSnapshot):
        """Save snapshot to JSON file"""
        with open(self.snapshot_file, 'w') as f:
            json.dump(snapshot.to_dict(), f, indent=2)
    
    def load_snapshot(self) -> Optional[ReadinessSnapshot]:
        """Load existing snapshot if available"""
        if self.snapshot_file.exists():
            with open(self.snapshot_file, 'r') as f:
                data = json.load(f)
                return ReadinessSnapshot.from_dict(data)
        return None
    
    def answer_next(self, answer: str) -> Tuple[ReadinessSnapshot, str]:
        """Process answer to the current question and update readiness"""
        snapshot = self.load_snapshot()
        if not snapshot:
            return self.analyze_opportunity(), "No snapshot found, created new analysis"
        
        # Find first unresolved gap
        for gap in snapshot.gaps:
            if not gap.resolved:
                gap.resolve(answer)
                
                # Process answer based on gap type
                if gap.id == "gfe_items" or gap.id == "gfe_clarify":
                    # Parse GFE items
                    if "no gfe" not in answer.lower():
                        snapshot.gfe_items = [item.strip() for item in answer.split(',')]
                
                elif gap.id == "supplier_quotes":
                    # Parse supplier quotes
                    if "standard pricing" not in answer.lower():
                        lines = answer.split('\n')
                        for line in lines:
                            if '|' in line:
                                parts = line.split('|')
                                if len(parts) >= 4:
                                    snapshot.vendor_quotes.append({
                                        "supplier": parts[0].strip(),
                                        "item": parts[1].strip() if len(parts) > 1 else "",
                                        "price": parts[2].strip() if len(parts) > 2 else "",
                                        "currency": parts[3].strip() if len(parts) > 3 else "USD"
                                    })
                
                elif gap.id == "competition":
                    # Parse competitors
                    if "unknown" not in answer.lower():
                        snapshot.competitors = [c.strip() for c in answer.split(',')]
                
                elif gap.id == "exclusions":
                    # Verify exclusions confirmed
                    if "confirmed" in answer.lower() and "no towers" in answer.lower():
                        snapshot.assumptions.append("Confirmed: NO towers, NO SC4200/4400, NO Silvus")
                
                break
        
        # Recalculate confidence
        self._calculate_confidence(snapshot)
        
        # Find next question
        unresolved = [g for g in snapshot.gaps if not g.resolved]
        if unresolved:
            # Prioritize critical gaps
            critical = [g for g in unresolved if g.critical]
            if critical:
                snapshot.suggested_next = critical[0].question
            else:
                snapshot.suggested_next = unresolved[0].question
        else:
            snapshot.suggested_next = None
        
        # Save updated snapshot
        self._save_snapshot(snapshot)
        
        # Generate response
        remaining = len(unresolved)
        confidence_pct = int(snapshot.confidence * 100)
        
        if confidence_pct >= 95:
            return snapshot, f"✓ Confidence: {confidence_pct}%. Ready to generate proposal!"
        elif remaining > 0:
            return snapshot, f"Confidence: {confidence_pct}%. {remaining} question(s) remaining."
        else:
            return snapshot, f"All questions answered. Confidence: {confidence_pct}%."
    
    def get_status(self) -> Dict[str, Any]:
        """Get current readiness status"""
        snapshot = self.load_snapshot()
        if not snapshot:
            return {
                "status": "Not analyzed",
                "message": "Run 'analyze' first to scan the opportunity"
            }
        
        unresolved = [g for g in snapshot.gaps if not g.resolved]
        confidence_pct = int(snapshot.confidence * 100)
        
        return {
            "confidence": confidence_pct,
            "ready": confidence_pct >= 95,
            "gaps_remaining": len(unresolved),
            "next_question": snapshot.suggested_next,
            "critical_gaps": [g.label for g in unresolved if g.critical],
            "files_analyzed": snapshot.files_scanned
        }
    
    def commit_readiness(self) -> Dict[str, Any]:
        """Commit readiness if confidence >= 95%"""
        snapshot = self.load_snapshot()
        if not snapshot:
            return {
                "success": False,
                "message": "No analysis found. Run 'analyze' first."
            }
        
        confidence_pct = int(snapshot.confidence * 100)
        
        if confidence_pct < 95:
            unresolved = [g for g in snapshot.gaps if not g.resolved]
            critical = [g for g in unresolved if g.critical]
            
            return {
                "success": False,
                "message": f"Cannot commit. Confidence {confidence_pct}% < 95%.",
                "next_action": f"Answer: {snapshot.suggested_next}" if snapshot.suggested_next else "Complete remaining gaps",
                "critical_gaps": len(critical),
                "total_gaps": len(unresolved)
            }
        
        # Generate meta.yaml from snapshot
        meta = {
            "client": "Dubai Police",  # Could be detected or asked
            "project": "Dismounted Soldier Communication Kit",
            "confidence": snapshot.confidence,
            "analysis_date": snapshot.timestamp,
            
            "equipment": {
                "detected": snapshot.detected_equipment,
                "confirmed": [g.answer for g in snapshot.gaps if g.id == "scope_clarity" and g.resolved]
            },
            
            "gfe_items": snapshot.gfe_items,
            "vendor_quotes": snapshot.vendor_quotes,
            "competitors": snapshot.competitors,
            
            "assumptions": snapshot.assumptions,
            "constraints": snapshot.constraints,
            
            "gaps_resolved": len([g for g in snapshot.gaps if g.resolved]),
            "total_gaps": len(snapshot.gaps)
        }
        
        meta_file = self.meta_dir / "draft.meta.yaml"
        with open(meta_file, 'w') as f:
            yaml.dump(meta, f, default_flow_style=False, sort_keys=False)
        
        return {
            "success": True,
            "message": f"✓ Readiness committed at {confidence_pct}% confidence",
            "meta_file": str(meta_file),
            "snapshot_file": str(self.snapshot_file)
        }


# CLI Interface
if __name__ == "__main__":
    import sys
    
    analyzer = ReadinessAnalyzer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "analyze":
            snapshot = analyzer.analyze_opportunity()
            status = analyzer.get_status()
            print(json.dumps({"message": "Analysis complete", **status}))
        
        elif command == "status":
            status = analyzer.get_status()
            print(json.dumps(status))
        
        elif command == "answer" and len(sys.argv) > 2:
            maybe_id = sys.argv[2]
            snapshot = analyzer.load_snapshot()
            if not snapshot:
                snapshot = analyzer.analyze_opportunity()
            
            gaps_by_id = {g.id: g for g in snapshot.gaps}
            if maybe_id in gaps_by_id and len(sys.argv) > 3:
                gap = gaps_by_id[maybe_id]
                answer_text = " ".join(sys.argv[3:]).strip()
                gap.answer = answer_text
                gap.resolved = bool(answer_text)
            else:
                # Fall back: apply to first unresolved (prefer critical)
                unresolved = [g for g in snapshot.gaps if not g.resolved]
                unresolved_crit = [g for g in unresolved if g.critical]
                target = unresolved_crit[0] if unresolved_crit else (unresolved[0] if unresolved else None)
                if target:
                    answer_text = " ".join(sys.argv[2:]).strip()
                    target.answer = answer_text
                    target.resolved = bool(answer_text)
            
            # Recalculate & persist
            analyzer._calculate_confidence(snapshot)
            analyzer._save_snapshot(snapshot)
            
            remaining = len([g for g in snapshot.gaps if not g.resolved])
            confidence_pct = int(snapshot.confidence * 100)
            next_q = None
            unresolved = [g for g in snapshot.gaps if not g.resolved]
            if unresolved:
                crit = [g for g in unresolved if g.critical]
                next_q = (crit[0] if crit else unresolved[0]).question
            print(json.dumps({"confidence": confidence_pct, "remaining": remaining, "next_question": next_q}))
        
        elif command == "commit":
            result = analyzer.commit_readiness()
            print(result['message'])
            if not result['success'] and result.get('next_action'):
                print(f"Next: {result['next_action']}")
        
        elif command == "park" and len(sys.argv) > 2:
            # Park a question for later
            gap_id = sys.argv[2]
            note = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else "Parked for later"
            snapshot = analyzer.load_snapshot()
            
            # Find and park the gap
            parked = False
            for gap in snapshot.gaps:
                if gap.id == gap_id:
                    gap.resolved = False
                    gap.answer = f"[PARKED] {note}"
                    parked = True
                    break
            
            if parked:
                analyzer._save_snapshot(snapshot)
                result = {
                    "status": "parked",
                    "gap_id": gap_id,
                    "note": note,
                    "message": f"Question '{gap_id}' parked: {note}"
                }
            else:
                result = {
                    "status": "error",
                    "message": f"Gap '{gap_id}' not found"
                }
            print(json.dumps(result))
        
        elif command == "reset":
            # Reset the session
            confirm = "--confirm" in sys.argv
            if confirm:
                if analyzer.snapshot_file.exists():
                    analyzer.snapshot_file.unlink()
                result = {
                    "status": "reset",
                    "message": "Session reset. All answers cleared."
                }
            else:
                result = {
                    "status": "error",
                    "message": "Reset requires --confirm flag"
                }
            print(json.dumps(result))
        
        elif command == "draft":
            # Generate draft with assumptions
            output_file = None
            for i, arg in enumerate(sys.argv):
                if arg == "--output" and i + 1 < len(sys.argv):
                    output_file = sys.argv[i + 1]
                    break
            
            snapshot = analyzer.load_snapshot()
            
            # Build draft metadata with assumptions
            assumptions_used = []
            for gap in snapshot.gaps:
                if not gap.resolved:
                    # Create assumption based on gap type
                    if gap.id == "scope_clarity":
                        assumption = "Assuming standard dismounted soldier kit with TETRA radio, Samsung device, INVISIO audio"
                    elif gap.id == "exclude_towers":
                        assumption = "Assuming towers, SC4200/4400, and Silvus are EXCLUDED"
                    elif gap.id == "device_model":
                        assumption = "Assuming Samsung S25 (latest model)"
                    elif gap.id == "quantity":
                        assumption = "Assuming 50 units (standard squad deployment)"
                    elif gap.id == "invisio_specs":
                        assumption = "Assuming INVISIO X7 with dual PTT and tactical earplugs"
                    elif gap.id == "mount_type":
                        assumption = "Assuming foldable mid-torso bunker kit"
                    else:
                        assumption = f"Using standard configuration for {gap.label}"
                    
                    assumptions_used.append({
                        "gap_id": gap.id,
                        "gap_label": gap.label,
                        "assumption": assumption,
                        "risk": "HIGH" if gap.critical else "MEDIUM"
                    })
            
            # Calculate draft confidence (lower than actual)
            draft_confidence = round((snapshot.confidence * 100) * 0.8, 1)  # as percent
            
            draft_meta = {
                "mode": "DRAFT",
                "confidence": draft_confidence,
                "assumptions_count": len(assumptions_used),
                "assumptions": assumptions_used,
                "warning": "This is a DRAFT with assumptions. Verify all assumptions before final generation.",
                "client": "Dubai Police",
                "project": "Dismounted Soldier Communication Kit",
                "equipment": {
                    "radio": "TETRA",
                    "device": "Samsung S25" if not any(g.resolved and g.answer and "S23" in g.answer for g in snapshot.gaps) else "Samsung S23",
                    "audio": "INVISIO X7 with dual PTT and tactical earplugs",
                    "mount": "Foldable mid-torso bunker kit"
                },
                "exclusions": ["towers", "SC4200", "SC4400", "Silvus radios"],
                "generated_at": datetime.now().isoformat()
            }
            
            # Save to file if requested
            if output_file:
                output_path = Path(output_file)
                with open(output_path, 'w') as f:
                    yaml.dump(draft_meta, f, default_flow_style=False, sort_keys=False)
                draft_meta["output_file"] = str(output_path)
            
            print(json.dumps(draft_meta, indent=2))
        
        else:
            print("Unknown command")
    
    else:
        print("Readiness Analyzer - Intelligent Gap Detection")
        print("Commands:")
        print("  python readiness_analyzer.py analyze    - Analyze opportunity")
        print("  python readiness_analyzer.py status     - Check readiness")
        print("  python readiness_analyzer.py answer ... - Answer current question")
        print("  python readiness_analyzer.py commit     - Commit when ready")