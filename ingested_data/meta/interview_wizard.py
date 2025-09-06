#!/usr/bin/env python3
"""
Metadata Interview Wizard for Dubai Police Dismounted Soldier Kit
One question at a time, explicit confirmations, no assumptions.
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

class Slot(Enum):
    CLIENT = "client"
    PROJECT = "project"
    DEVICE_MODEL = "device_model"
    CONFIRM_RADIO_TETRA = "confirm_radio_tetra"
    CONFIRM_INVISIO = "confirm_invisio"
    CONFIRM_MOUNT = "confirm_mount"
    DECLARE_EXCLUSIONS = "declare_exclusions"
    GFE_ITEMS = "gfe_items"
    SUPPLIER_QUOTES = "supplier_quotes"
    PRICING_SUMMARY = "pricing_summary"
    FINAL_READBACK = "final_readback"

class InterviewWizard:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.meta_dir = self.project_root / "ingested_data" / "meta"
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        
        self.session_file = self.meta_dir / "session.json"
        self.draft_file = self.meta_dir / "draft.meta.yaml"
        
        self.questions = [
            {
                "slot": Slot.CLIENT,
                "prompt": "Who is the customer? (e.g., 'Dubai Police')",
                "validator": self._validate_text
            },
            {
                "slot": Slot.PROJECT,
                "prompt": "What is the project name/title? (e.g., 'Dismounted Soldier Communication Kit')",
                "validator": self._validate_text
            },
            {
                "slot": Slot.DEVICE_MODEL,
                "prompt": "Which Samsung device model? Type 'S23' or 'S25':",
                "validator": self._validate_device
            },
            {
                "slot": Slot.CONFIRM_RADIO_TETRA,
                "prompt": "Confirm radio system = TETRA? Type 'yes' to confirm:",
                "validator": self._validate_yes_no
            },
            {
                "slot": Slot.CONFIRM_INVISIO,
                "prompt": "Confirm audio = INVISIO dual PTT + earplugs? Type 'yes' to confirm:",
                "validator": self._validate_yes_no
            },
            {
                "slot": Slot.CONFIRM_MOUNT,
                "prompt": "Confirm mount = foldable mid-torso bunker kit? Type 'yes' to confirm:",
                "validator": self._validate_yes_no
            },
            {
                "slot": Slot.DECLARE_EXCLUSIONS,
                "prompt": "IMPORTANT: Explicitly confirm these are EXCLUDED from scope:\n  - Towers\n  - SC4200/SC4400\n  - Silvus radios\nType 'exclude confirmed' to proceed:",
                "validator": self._validate_exclusion
            },
            {
                "slot": Slot.GFE_ITEMS,
                "prompt": "List any Government Furnished Equipment (GFE) items, comma-separated.\nExample: 'TETRA radios, antennas'\nOr type 'none' if no GFE:",
                "validator": self._validate_gfe
            },
            {
                "slot": Slot.SUPPLIER_QUOTES,
                "prompt": "Enter supplier quotes (or type 'skip' if none).\nFormat per line: Supplier | Item | PartNumber | Currency | UnitPrice | Qty | ObtainedBy | QuoteRef\nExample: INVISIO | X7 Earplug | X7-EP | USD | 450 | 50 | customer | Q-2024-001\nEnter quotes (end with blank line):",
                "validator": self._validate_quotes
            },
            {
                "slot": Slot.PRICING_SUMMARY,
                "prompt": "Enter pricing summary or type 'skip':\nFormat: Currency=USD, Equipment=237500, Services=43000, Contingency=10",
                "validator": self._validate_pricing
            }
        ]
        
    def load_session(self) -> Dict[str, Any]:
        """Load saved session or create new one"""
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                return json.load(f)
        return {
            "step": 0,
            "slots": {},
            "history": [],
            "status": "in_progress"
        }
    
    def save_session(self, session: Dict[str, Any]):
        """Save session state"""
        with open(self.session_file, 'w') as f:
            json.dump(session, f, indent=2)
    
    def _validate_text(self, value: str) -> str:
        """Validate non-empty text"""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Cannot be empty")
        return cleaned
    
    def _validate_device(self, value: str) -> str:
        """Validate Samsung device model"""
        upper = value.upper().strip()
        if "23" in upper or "S23" in upper:
            return "Samsung S23"
        elif "25" in upper or "S25" in upper:
            return "Samsung S25"
        else:
            raise ValueError("Must be S23 or S25")
    
    def _validate_yes_no(self, value: str) -> bool:
        """Validate yes/no confirmation"""
        lower = value.lower().strip()
        if lower in ["yes", "y", "confirm", "confirmed"]:
            return True
        elif lower in ["no", "n"]:
            return False
        else:
            raise ValueError("Please type 'yes' or 'no'")
    
    def _validate_exclusion(self, value: str) -> bool:
        """Validate exclusion confirmation"""
        lower = value.lower().strip()
        if "exclude" in lower and "confirm" in lower:
            return True
        raise ValueError("Type 'exclude confirmed' to proceed")
    
    def _validate_gfe(self, value: str) -> List[str]:
        """Parse GFE items"""
        cleaned = value.strip()
        if cleaned.lower() == "none":
            return []
        items = [item.strip() for item in cleaned.split(",")]
        return [item for item in items if item]
    
    def _validate_quotes(self, value: str) -> List[Dict[str, Any]]:
        """Parse supplier quotes"""
        if value.lower().strip() == "skip":
            return []
        
        quotes = []
        lines = value.strip().split("\n")
        
        for line in lines:
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 6:
                continue
                
            quote = {
                "supplier": parts[0],
                "item": parts[1],
                "part_number": parts[2] if len(parts) > 2 else "",
                "currency": parts[3] if len(parts) > 3 else "USD",
                "unit_price": float(parts[4].replace(",", "").replace("$", "")) if len(parts) > 4 else 0,
                "qty": int(parts[5]) if len(parts) > 5 else 1,
                "obtained_by": parts[6] if len(parts) > 6 else "customer",
                "quote_ref": parts[7] if len(parts) > 7 else ""
            }
            quotes.append(quote)
        
        return quotes
    
    def _validate_pricing(self, value: str) -> Optional[Dict[str, Any]]:
        """Parse pricing summary"""
        if value.lower().strip() == "skip":
            return None
        
        pricing = {}
        parts = value.split(",")
        
        for part in parts:
            if "=" in part:
                key, val = part.split("=", 1)
                key = key.strip().lower()
                val = val.strip()
                
                if key == "currency":
                    pricing["currency"] = val.upper()
                elif key == "equipment":
                    pricing["equipment_total"] = float(val.replace(",", "").replace("$", ""))
                elif key == "services":
                    pricing["services_total"] = float(val.replace(",", "").replace("$", ""))
                elif key == "contingency":
                    pricing["contingency_pct"] = float(val.replace("%", ""))
        
        return pricing if pricing else None
    
    def get_next_question(self, session: Dict[str, Any]) -> Optional[str]:
        """Get the next question to ask"""
        step = session.get("step", 0)
        if step < len(self.questions):
            return self.questions[step]["prompt"]
        return None
    
    def process_answer(self, answer: str, user_id: str = "user") -> Dict[str, Any]:
        """Process user's answer and advance to next question"""
        session = self.load_session()
        step = session.get("step", 0)
        
        if step >= len(self.questions):
            return {
                "status": "complete",
                "message": "Interview complete. Type 'commit' to save metadata."
            }
        
        question = self.questions[step]
        
        try:
            # Validate and store answer
            validated_value = question["validator"](answer)
            session["slots"][question["slot"].value] = validated_value
            session["history"].append({
                "slot": question["slot"].value,
                "value": validated_value,
                "timestamp": datetime.now().isoformat()
            })
            
            # Move to next question
            session["step"] = step + 1
            self.save_session(session)
            
            # Get next question or finish
            next_q = self.get_next_question(session)
            if next_q:
                return {
                    "status": "continue",
                    "message": next_q
                }
            else:
                readback = self.generate_readback(session)
                return {
                    "status": "ready_to_commit",
                    "message": f"Review your entries:\n\n{readback}\n\nType 'approve' to commit or 'back' to edit."
                }
                
        except ValueError as e:
            return {
                "status": "error",
                "message": f"Invalid input: {e}\nPlease try again:"
            }
    
    def go_back(self) -> str:
        """Go back to previous question"""
        session = self.load_session()
        session["step"] = max(0, session["step"] - 1)
        self.save_session(session)
        
        question = self.get_next_question(session)
        return question if question else "At beginning of interview."
    
    def generate_readback(self, session: Dict[str, Any]) -> str:
        """Generate human-readable summary of collected data"""
        slots = session.get("slots", {})
        
        lines = [
            f"Client: {slots.get('client', 'Not set')}",
            f"Project: {slots.get('project', 'Not set')}",
            f"Device: {slots.get('device_model', 'Not set')}",
            f"Radio: TETRA (confirmed: {slots.get('confirm_radio_tetra', False)})",
            f"Audio: INVISIO dual PTT + earplugs (confirmed: {slots.get('confirm_invisio', False)})",
            f"Mount: Foldable mid-torso bunker kit (confirmed: {slots.get('confirm_mount', False)})",
            f"Exclusions confirmed: {slots.get('declare_exclusions', False)}",
            f"  - NO towers, NO SC4200/4400, NO Silvus",
            f"GFE items: {', '.join(slots.get('gfe_items', [])) or 'None'}",
            f"Supplier quotes: {len(slots.get('supplier_quotes', []))} items",
        ]
        
        if slots.get('pricing_summary'):
            ps = slots['pricing_summary']
            lines.append(f"Pricing: {ps.get('currency', 'USD')} Equipment={ps.get('equipment_total', 0):,.2f} Services={ps.get('services_total', 0):,.2f}")
        
        return "\n".join(lines)
    
    def commit_metadata(self, user_id: str = "user") -> Dict[str, Any]:
        """Commit the collected metadata to draft.meta.yaml"""
        session = self.load_session()
        slots = session.get("slots", {})
        
        # Validate required fields
        required = ["client", "project", "device_model", "confirm_radio_tetra", 
                   "confirm_invisio", "confirm_mount", "declare_exclusions"]
        
        missing = [r for r in required if r not in slots]
        if missing:
            return {
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing)}"
            }
        
        # Check exclusions are confirmed
        if not slots.get("declare_exclusions"):
            return {
                "status": "error",
                "message": "Exclusions not confirmed. Run interview again."
            }
        
        # Build metadata structure
        meta = {
            "client": slots["client"],
            "project": slots["project"],
            "version": "v1.0",
            "brand": "beacon-red",
            
            "scope_summary": f"Dismounted soldier communication kit for {slots['client']} featuring TETRA radio, {slots['device_model']}, INVISIO audio system with dual PTT, and foldable mid-torso bunker kit.",
            
            "equipment": {
                "radio_system": "TETRA",
                "device_model": slots["device_model"],
                "audio": {
                    "ptt": "INVISIO dual PTT",
                    "earplugs": "INVISIO earplugs"
                },
                "mount": "foldable mid-torso bunker kit"
            },
            
            "explicit_exclusions": [
                "towers",
                "SC4200",
                "SC4400",
                "Silvus radios"
            ],
            
            "gfe_items": slots.get("gfe_items", []),
            "supplier_quotes": slots.get("supplier_quotes", []),
            
            "provenance": {
                "created_by": user_id,
                "created_at": datetime.now().isoformat(),
                "interview_completed": True,
                "confirmations": [
                    "radio_tetra",
                    "invisio_audio",
                    "bunker_mount",
                    "exclusions"
                ]
            }
        }
        
        if slots.get("pricing_summary"):
            meta["pricing_summary"] = slots["pricing_summary"]
        
        # Write to YAML
        with open(self.draft_file, 'w') as f:
            yaml.dump(meta, f, default_flow_style=False, sort_keys=False)
        
        # Mark session as complete
        session["status"] = "committed"
        session["committed_at"] = datetime.now().isoformat()
        self.save_session(session)
        
        return {
            "status": "success",
            "message": f"Metadata committed to: {self.draft_file}\nYou can now run 'generate proposal' with confidence.",
            "path": str(self.draft_file)
        }
    
    def reset(self):
        """Reset the interview session"""
        if self.session_file.exists():
            self.session_file.unlink()
        return "Interview session reset. Type 'begin interview' to start fresh."


# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    wizard = InterviewWizard()
    
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        
        if command == "begin" or command == "start":
            wizard.reset()
            session = wizard.load_session()
            print(wizard.get_next_question(session))
        
        elif command == "back":
            print(wizard.go_back())
        
        elif command == "show" or command == "status":
            session = wizard.load_session()
            print(wizard.generate_readback(session))
        
        elif command == "commit" or command == "approve":
            result = wizard.commit_metadata()
            print(result["message"])
        
        elif command == "reset":
            print(wizard.reset())
        
        else:
            # Treat as answer to current question
            result = wizard.process_answer(command)
            print(result["message"])
    else:
        print("Interview Wizard for Dubai Police Dismounted Soldier Kit")
        print("Commands:")
        print("  python interview_wizard.py begin    - Start interview")
        print("  python interview_wizard.py back     - Go to previous question")
        print("  python interview_wizard.py show     - Show current status")
        print("  python interview_wizard.py commit   - Save metadata")
        print("  python interview_wizard.py reset    - Clear session")
        print("  python interview_wizard.py [answer] - Answer current question")