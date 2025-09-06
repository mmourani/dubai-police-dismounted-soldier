#!/usr/bin/env python3
"""
Enhanced Readiness Analyzer v2 - Two-Mode System
Mode 1: Gap Analysis with question routing (who to ask)
Mode 2: Draft Generation with explicit assumptions
"""

import json
import yaml
import re
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

class QuestionStatus(Enum):
    UNANSWERED = "unanswered"
    PENDING = "pending"  # Sent to stakeholder, awaiting response
    ANSWERED = "answered"
    ASSUMED = "assumed"  # Used assumption for draft

@dataclass
class Question:
    """Enhanced gap with routing information"""
    id: str
    question: str
    who_to_ask: str  # SupplierX, Customer, Engineering, End-User, Market Intelligence
    why_matters: str
    critical: bool
    weight: float
    status: QuestionStatus = QuestionStatus.UNANSWERED
    answer: Optional[str] = None
    assumption: Optional[str] = None  # What we'll assume if unanswered
    assumption_rationale: Optional[str] = None
    date_identified: str = field(default_factory=lambda: datetime.now().isoformat())
    date_answered: Optional[str] = None
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Question':
        if 'status' in data:
            data['status'] = QuestionStatus(data['status'])
        return cls(**data)

@dataclass
class ReadinessSnapshot:
    """Enhanced snapshot with question routing and assumptions"""
    timestamp: str
    project_root: str
    mode: str = "analysis"  # "analysis" or "draft"
    
    # Discovery
    files_scanned: int = 0
    detected_equipment: List[str] = field(default_factory=list)
    detected_pricing: List[str] = field(default_factory=list)
    detected_exclusions: List[str] = field(default_factory=list)
    
    # Structured data
    confirmed_scope: Optional[str] = None
    gfe_items: List[str] = field(default_factory=list)
    vendor_quotes: List[Dict] = field(default_factory=list)
    competitors: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    
    # Questions with routing
    questions: List[Question] = field(default_factory=list)
    
    # Assumptions for draft mode
    assumptions_used: List[Dict] = field(default_factory=list)
    
    # Scoring
    confidence: float = 0.0
    draft_confidence: float = 0.0  # Confidence if we use assumptions
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['questions'] = [q.to_dict() for q in self.questions]
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ReadinessSnapshot':
        questions_data = data.pop('questions', [])
        snapshot = cls(**data)
        snapshot.questions = [Question.from_dict(q) for q in questions_data]
        return snapshot

class EnhancedReadinessAnalyzer:
    """Two-mode analyzer: Gap Analysis + Draft Generation"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.meta_dir = self.project_root / "ingested_data" / "meta"
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        
        self.snapshot_file = self.meta_dir / "opportunity.readiness.json"
        self.draft_file = self.meta_dir / "draft.meta.yaml"
        self.assumptions_file = self.meta_dir / "assumptions.yaml"
        
        # Domain knowledge for smart assumptions
        self.default_assumptions = {
            "device_model": "Samsung S25 (latest model, conservative choice)",
            "delivery": "90 days from PO (industry standard)",
            "payment": "30/40/20/10 payment terms (standard for government)",
            "environmental": "IP67, MIL-STD-810G (standard tactical requirements)",
            "competitors": "Motorola Solutions, Harris Corporation (usual suspects)",
            "pricing_markup": "15% markup on list prices (industry average)"
        }
    
    def analyze_opportunity(self) -> ReadinessSnapshot:
        """Analyze and generate questions with routing"""
        # Load previous if exists (merge mode)
        prev = self.load_snapshot()
        prev_answers = {}
        if prev:
            prev_answers = {q.id: q for q in prev.questions if q.status == QuestionStatus.ANSWERED}
        
        snapshot = ReadinessSnapshot(
            timestamp=datetime.now().isoformat(),
            project_root=str(self.project_root),
            mode="analysis"
        )
        
        # Scan files
        self._scan_and_detect(snapshot)
        
        # Generate questions with routing
        questions = []
        
        # 1. Scope confirmation (Customer)
        questions.append(Question(
            id="scope_confirmation",
            question="Confirm complete equipment scope: TETRA radio + Samsung device model + INVISIO audio + mount type",
            who_to_ask="Customer",
            why_matters="Defines entire solution architecture and pricing",
            critical=True,
            weight=0.25,
            assumption="TETRA handheld + Samsung S25 + INVISIO dual PTT/earplugs + foldable torso mount",
            assumption_rationale="Based on latest RFQ patterns and market trends"
        ))
        
        # 2. Exclusions (Customer) - only if keywords detected
        if snapshot.detected_exclusions:
            questions.append(Question(
                id="exclusions",
                question="Confirm these are EXCLUDED: towers, SC4200/4400, Silvus radios",
                who_to_ask="Customer",
                why_matters="Prevents scope creep and wrong pricing",
                critical=True,
                weight=0.20,
                assumption="NO towers, NO SC4200/4400, NO Silvus radios",
                assumption_rationale="Dismounted soldier kit typically excludes infrastructure"
            ))
        
        # 3. GFE Declaration (Customer/Procurement)
        questions.append(Question(
            id="gfe_items",
            question="Which items are Government Furnished Equipment (GFE)?",
            who_to_ask="Customer Procurement",
            why_matters="GFE items must not be priced in our proposal",
            critical=True,
            weight=0.15,
            assumption="TETRA radios and Samsung devices are GFE",
            assumption_rationale="Common pattern for government contracts"
        ))
        
        # 4. Supplier Quotes (Suppliers)
        questions.append(Question(
            id="invisio_quote",
            question="Current quote for INVISIO dual PTT X7 system (50 units)",
            who_to_ask="INVISIO / SupplierX",
            why_matters="Accurate pricing for major cost component",
            critical=True,
            weight=0.10,
            assumption="USD 480 per unit (last known price + 5% inflation)",
            assumption_rationale="Based on Q3 2024 pricing with inflation adjustment"
        ))
        
        questions.append(Question(
            id="mount_quote",
            question="Quote for foldable torso mount/bunker kit (50 units)",
            who_to_ask="Bunker Supply / SupplierY",
            why_matters="Significant cost item requiring current pricing",
            critical=True,
            weight=0.10,
            assumption="USD 320 per unit",
            assumption_rationale="Catalog price from similar recent projects"
        ))
        
        # 5. Technical Requirements (Engineering)
        questions.append(Question(
            id="operational_env",
            question="Confirm environmental specs: IP rating, temperature range, runtime",
            who_to_ask="Engineering Team",
            why_matters="Determines product selection and compliance requirements",
            critical=False,
            weight=0.10,
            assumption="IP67, -20°C to +55°C, 8-hour runtime",
            assumption_rationale="Standard Dubai Police tactical requirements"
        ))
        
        # 6. Competitive Intelligence (Market Intelligence)
        questions.append(Question(
            id="competitors",
            question="Identify competing vendors for this opportunity",
            who_to_ask="Market Intelligence / Sales",
            why_matters="Shapes win themes and pricing strategy",
            critical=False,
            weight=0.05,
            assumption="Motorola Solutions, Harris Corporation, Hytera",
            assumption_rationale="Usual competitors in MENA region tactical comms"
        ))
        
        # 7. Delivery & Payment (Customer/Commercial)
        questions.append(Question(
            id="delivery_terms",
            question="Required delivery timeline and payment terms",
            who_to_ask="Customer Commercial Team",
            why_matters="Affects cash flow and project scheduling",
            critical=False,
            weight=0.05,
            assumption="90 days delivery, 30/40/20/10 payment terms",
            assumption_rationale="Standard government contract terms"
        ))
        
        # Merge with previous answers
        for q in questions:
            if q.id in prev_answers:
                prev_q = prev_answers[q.id]
                q.status = prev_q.status
                q.answer = prev_q.answer
                q.date_answered = prev_q.date_answered
        
        snapshot.questions = questions
        
        # Calculate confidence
        self._calculate_confidence(snapshot)
        
        # Save
        self._save_snapshot(snapshot)
        
        return snapshot
    
    def _scan_and_detect(self, snapshot: ReadinessSnapshot):
        """Scan files and detect context"""
        # Count files
        for ext in [".md", ".pdf", ".csv", ".docx"]:
            files = list(self.project_root.rglob(f"*{ext}"))
            snapshot.files_scanned += len(files)
        
        # Sample content from markdown files
        md_files = list(self.project_root.rglob("*.md"))[:20]
        content = ""
        for f in md_files:
            try:
                content += f.read_text(errors='ignore')[:5000]
            except:
                pass
        
        # Detect patterns
        if re.search(r'\bTETRA\b', content, re.I):
            snapshot.detected_equipment.append("TETRA radio")
        if re.search(r'\bS23\b', content):
            snapshot.detected_equipment.append("Samsung S23")
        if re.search(r'\bS25\b', content):
            snapshot.detected_equipment.append("Samsung S25")
        if re.search(r'\bINVISIO\b', content, re.I):
            snapshot.detected_equipment.append("INVISIO audio")
        
        # Detect exclusion keywords
        if re.search(r'\b(tower|SC4[24]00|Silvus)\b', content, re.I):
            snapshot.detected_exclusions.append("Infrastructure keywords detected")
        
        # Detect pricing
        prices = re.findall(r'(?:USD|AED|\$)\s*[\d,]+(?:\.\d{2})?', content)
        snapshot.detected_pricing = prices[:10]
    
    def _calculate_confidence(self, snapshot: ReadinessSnapshot):
        """Calculate both actual and potential confidence"""
        base = 0.15 if snapshot.files_scanned > 0 else 0.0
        
        # Actual confidence (answered questions only)
        answered_weight = sum(q.weight for q in snapshot.questions 
                             if q.status == QuestionStatus.ANSWERED)
        unanswered_critical = sum(q.weight * 0.5 for q in snapshot.questions 
                                 if q.critical and q.status != QuestionStatus.ANSWERED)
        
        snapshot.confidence = max(0.0, min(1.0, base + answered_weight - unanswered_critical))
        
        # Draft confidence (with assumptions)
        all_weight = sum(q.weight for q in snapshot.questions)
        snapshot.draft_confidence = min(1.0, base + all_weight * 0.85)  # 85% credit for assumptions
    
    def get_status(self) -> Dict[str, Any]:
        """Get current readiness status with question routing"""
        snapshot = self.load_snapshot()
        if not snapshot:
            return {"status": "Not analyzed", "message": "Run 'analyze' first"}
        
        # Group questions by who to ask
        by_stakeholder = {}
        for q in snapshot.questions:
            if q.status != QuestionStatus.ANSWERED:
                if q.who_to_ask not in by_stakeholder:
                    by_stakeholder[q.who_to_ask] = []
                by_stakeholder[q.who_to_ask].append({
                    "id": q.id,
                    "question": q.question,
                    "critical": q.critical,
                    "status": q.status.value
                })
        
        confidence_pct = int(snapshot.confidence * 100)
        draft_confidence_pct = int(snapshot.draft_confidence * 100)
        
        return {
            "confidence": confidence_pct,
            "draft_confidence": draft_confidence_pct,
            "ready_for_final": confidence_pct >= 95,
            "ready_for_draft": draft_confidence_pct >= 75,
            "questions_by_stakeholder": by_stakeholder,
            "total_questions": len(snapshot.questions),
            "answered": len([q for q in snapshot.questions if q.status == QuestionStatus.ANSWERED]),
            "mode": snapshot.mode
        }
    
    def answer_question(self, question_id: str, answer: str) -> Tuple[bool, str]:
        """Answer a specific question"""
        snapshot = self.load_snapshot()
        if not snapshot:
            return False, "No analysis found. Run 'analyze' first"
        
        for q in snapshot.questions:
            if q.id == question_id:
                q.answer = answer
                q.status = QuestionStatus.ANSWERED
                q.date_answered = datetime.now().isoformat()
                
                # Process answer based on type
                if q.id == "gfe_items":
                    snapshot.gfe_items = [item.strip() for item in answer.split(',')]
                elif q.id == "scope_confirmation":
                    snapshot.confirmed_scope = answer
                elif q.id == "competitors":
                    snapshot.competitors = [c.strip() for c in answer.split(',')]
                elif "quote" in q.id:
                    # Parse supplier quote
                    parts = answer.split('|')
                    if len(parts) >= 4:
                        snapshot.vendor_quotes.append({
                            "supplier": parts[0].strip(),
                            "item": parts[1].strip() if len(parts) > 1 else "",
                            "price": parts[2].strip() if len(parts) > 2 else "",
                            "currency": parts[3].strip() if len(parts) > 3 else "USD",
                            "qty": parts[4].strip() if len(parts) > 4 else "1"
                        })
                
                self._calculate_confidence(snapshot)
                self._save_snapshot(snapshot)
                
                return True, f"Answer recorded. Confidence now: {int(snapshot.confidence*100)}%"
        
        return False, f"Question '{question_id}' not found"
    
    def mark_pending(self, question_id: str, notes: str = "") -> Tuple[bool, str]:
        """Mark question as pending (sent to stakeholder)"""
        snapshot = self.load_snapshot()
        if not snapshot:
            return False, "No analysis found"
        
        for q in snapshot.questions:
            if q.id == question_id:
                q.status = QuestionStatus.PENDING
                self._save_snapshot(snapshot)
                return True, f"Marked '{question_id}' as pending. Notes: {notes}"
        
        return False, f"Question '{question_id}' not found"
    
    def generate_draft(self) -> Dict[str, Any]:
        """Generate draft proposal with explicit assumptions"""
        snapshot = self.load_snapshot()
        if not snapshot:
            return {"success": False, "message": "No analysis found"}
        
        snapshot.mode = "draft"
        assumptions_used = []
        
        # Process each unanswered question
        for q in snapshot.questions:
            if q.status != QuestionStatus.ANSWERED:
                q.status = QuestionStatus.ASSUMED
                assumptions_used.append({
                    "id": q.id,
                    "question": q.question,
                    "assumption": q.assumption,
                    "rationale": q.assumption_rationale,
                    "who_should_confirm": q.who_to_ask,
                    "risk": "HIGH" if q.critical else "MEDIUM"
                })
        
        snapshot.assumptions_used = assumptions_used
        
        # Generate draft metadata
        draft_meta = {
            "mode": "DRAFT",
            "generated": datetime.now().isoformat(),
            "confidence": int(snapshot.confidence * 100),
            "draft_confidence": int(snapshot.draft_confidence * 100),
            
            "client": "Dubai Police",
            "project": "Dismounted Soldier Communication Kit",
            
            "scope": snapshot.confirmed_scope or snapshot.questions[0].assumption,
            
            "equipment": {
                "confirmed": snapshot.detected_equipment,
                "assumed": [q.assumption for q in snapshot.questions 
                          if "scope" in q.id and q.status == QuestionStatus.ASSUMED]
            },
            
            "gfe_items": snapshot.gfe_items or ["TETRA radios (assumed)", "Samsung devices (assumed)"],
            
            "pricing": {
                "vendor_quotes": snapshot.vendor_quotes,
                "assumptions": [a for a in assumptions_used if "quote" in a["id"]]
            },
            
            "assumptions_tracker": assumptions_used,
            
            "warnings": [
                f"⚠️ This is a DRAFT with {len(assumptions_used)} assumptions",
                f"⚠️ Confidence: {int(snapshot.confidence*100)}% (target: 95%)",
                f"⚠️ Critical assumptions need validation from: " + 
                ", ".join(set(a["who_should_confirm"] for a in assumptions_used if a["risk"] == "HIGH"))
            ]
        }
        
        # Save draft metadata
        with open(self.draft_file, 'w') as f:
            yaml.dump(draft_meta, f, default_flow_style=False, sort_keys=False)
        
        # Save assumptions separately for tracking
        with open(self.assumptions_file, 'w') as f:
            yaml.dump({"assumptions": assumptions_used, "generated": datetime.now().isoformat()}, f)
        
        self._save_snapshot(snapshot)
        
        return {
            "success": True,
            "message": f"Draft generated with {len(assumptions_used)} assumptions",
            "confidence": int(snapshot.confidence * 100),
            "draft_confidence": int(snapshot.draft_confidence * 100),
            "draft_file": str(self.draft_file),
            "assumptions_file": str(self.assumptions_file),
            "critical_validations_needed": [a["who_should_confirm"] for a in assumptions_used if a["risk"] == "HIGH"]
        }
    
    def commit_final(self) -> Dict[str, Any]:
        """Commit final proposal (requires 95% confidence)"""
        snapshot = self.load_snapshot()
        if not snapshot:
            return {"success": False, "message": "No analysis found"}
        
        confidence_pct = int(snapshot.confidence * 100)
        
        if confidence_pct < 95:
            unanswered = [q for q in snapshot.questions if q.status != QuestionStatus.ANSWERED]
            return {
                "success": False,
                "message": f"Cannot commit. Confidence {confidence_pct}% < 95%",
                "unanswered_questions": len(unanswered),
                "blocking_items": [{"id": q.id, "who_to_ask": q.who_to_ask} for q in unanswered if q.critical]
            }
        
        # Generate final metadata (no assumptions)
        final_meta = {
            "mode": "FINAL",
            "generated": datetime.now().isoformat(),
            "confidence": confidence_pct,
            
            "client": "Dubai Police",
            "project": "Dismounted Soldier Communication Kit",
            
            "scope": snapshot.confirmed_scope,
            "gfe_items": snapshot.gfe_items,
            "vendor_quotes": snapshot.vendor_quotes,
            "competitors": snapshot.competitors,
            
            "validated_by": list(set(q.who_to_ask for q in snapshot.questions 
                                    if q.status == QuestionStatus.ANSWERED)),
            
            "audit_trail": {
                "questions_asked": len(snapshot.questions),
                "questions_answered": len([q for q in snapshot.questions 
                                          if q.status == QuestionStatus.ANSWERED]),
                "analysis_started": min(q.date_identified for q in snapshot.questions),
                "analysis_completed": datetime.now().isoformat()
            }
        }
        
        final_file = self.meta_dir / "final.meta.yaml"
        with open(final_file, 'w') as f:
            yaml.dump(final_meta, f, default_flow_style=False, sort_keys=False)
        
        return {
            "success": True,
            "message": f"✅ Final proposal ready at {confidence_pct}% confidence",
            "final_file": str(final_file)
        }
    
    def _save_snapshot(self, snapshot: ReadinessSnapshot):
        """Save snapshot to JSON"""
        with open(self.snapshot_file, 'w') as f:
            json.dump(snapshot.to_dict(), f, indent=2)
    
    def load_snapshot(self) -> Optional[ReadinessSnapshot]:
        """Load existing snapshot"""
        if self.snapshot_file.exists():
            with open(self.snapshot_file, 'r') as f:
                data = json.load(f)
                return ReadinessSnapshot.from_dict(data)
        return None


# CLI Interface
if __name__ == "__main__":
    import sys
    
    analyzer = EnhancedReadinessAnalyzer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "analyze":
            snapshot = analyzer.analyze_opportunity()
            status = analyzer.get_status()
            print(f"Analysis complete!")
            print(f"Confidence: {status['confidence']}% (Final: need 95%)")
            print(f"Draft possible at: {status['draft_confidence']}%")
            print(f"\nQuestions by stakeholder:")
            for stakeholder, questions in status['questions_by_stakeholder'].items():
                print(f"\n{stakeholder}:")
                for q in questions:
                    mark = "🔴" if q['critical'] else "🟡"
                    print(f"  {mark} [{q['id']}] {q['question']}")
        
        elif command == "status":
            status = analyzer.get_status()
            print(f"Confidence: {status['confidence']}% (need 95% for final)")
            print(f"Draft confidence: {status['draft_confidence']}%")
            print(f"Questions: {status['answered']}/{status['total_questions']} answered")
            
            if status['questions_by_stakeholder']:
                print("\nOutstanding questions by stakeholder:")
                for stakeholder, questions in status['questions_by_stakeholder'].items():
                    print(f"  {stakeholder}: {len(questions)} questions")
        
        elif command == "answer" and len(sys.argv) > 3:
            question_id = sys.argv[2]
            answer = " ".join(sys.argv[3:])
            success, message = analyzer.answer_question(question_id, answer)
            print(message)
        
        elif command == "pending" and len(sys.argv) > 2:
            question_id = sys.argv[2]
            notes = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
            success, message = analyzer.mark_pending(question_id, notes)
            print(message)
        
        elif command == "draft":
            result = analyzer.generate_draft()
            if result['success']:
                print(f"✅ {result['message']}")
                print(f"Confidence: {result['confidence']}% (actual)")
                print(f"Draft confidence: {result['draft_confidence']}% (with assumptions)")
                print(f"\nFiles generated:")
                print(f"  - Draft: {result['draft_file']}")
                print(f"  - Assumptions: {result['assumptions_file']}")
                if result['critical_validations_needed']:
                    print(f"\n⚠️ Critical validations needed from:")
                    for stakeholder in set(result['critical_validations_needed']):
                        print(f"  - {stakeholder}")
            else:
                print(f"❌ {result['message']}")
        
        elif command == "commit":
            result = analyzer.commit_final()
            if result['success']:
                print(result['message'])
                print(f"Final proposal: {result.get('final_file', '')}")
            else:
                print(f"❌ {result['message']}")
                if result.get('blocking_items'):
                    print("\nBlocking items:")
                    for item in result['blocking_items']:
                        print(f"  - [{item['id']}] Ask: {item['who_to_ask']}")
        
        else:
            print("Unknown command or missing arguments")
    
    else:
        print("Enhanced Readiness Analyzer v2 - Two-Mode System")
        print("\nCommands:")
        print("  python readiness_analyzer_v2.py analyze          - Analyze opportunity")
        print("  python readiness_analyzer_v2.py status           - Check readiness")
        print("  python readiness_analyzer_v2.py answer <id> ...  - Answer specific question")
        print("  python readiness_analyzer_v2.py pending <id> ... - Mark as sent to stakeholder")
        print("  python readiness_analyzer_v2.py draft            - Generate draft with assumptions")
        print("  python readiness_analyzer_v2.py commit           - Commit final (requires 95%)")
        print("\nExample:")
        print("  python readiness_analyzer_v2.py answer invisio_quote 'INVISIO | X7 PTT | 480 | USD | 50'")