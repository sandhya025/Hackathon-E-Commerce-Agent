"""
Case Memory — Persistent JSON-Based Case History Store

Provides the agent with long-term memory across support ticket resolutions:
- Stores each case's verdict, reasoning, and fraud signals
- Tracks per-customer fraud patterns (repeat offenders)
- Enables cross-case pattern recognition

Memory is persisted to disk as JSON files in memory/store/.
"""

import json
import os
from datetime import datetime


class CaseMemory:
    """Persistent memory store for dispute resolution cases."""

    def __init__(self, memory_dir: str = None):
        if memory_dir is None:
            memory_dir = os.path.join(os.path.dirname(__file__), "store")
        os.makedirs(memory_dir, exist_ok=True)

        self.memory_dir = memory_dir
        self.case_history_file = os.path.join(memory_dir, "case_history.json")
        self.fraud_patterns_file = os.path.join(memory_dir, "fraud_patterns.json")
        self._load()

    def _load(self):
        """Load memory from disk."""
        if os.path.exists(self.case_history_file):
            with open(self.case_history_file, "r", encoding="utf-8") as f:
                self.case_history = json.load(f)
        else:
            self.case_history = {}

        if os.path.exists(self.fraud_patterns_file):
            with open(self.fraud_patterns_file, "r", encoding="utf-8") as f:
                self.fraud_patterns = json.load(f)
        else:
            self.fraud_patterns = {}

    def _save(self):
        """Persist memory to disk."""
        with open(self.case_history_file, "w", encoding="utf-8") as f:
            json.dump(self.case_history, f, indent=2)
        with open(self.fraud_patterns_file, "w", encoding="utf-8") as f:
            json.dump(self.fraud_patterns, f, indent=2)

    def store(self, case_data: dict, verdict: dict):
        """
        Store a resolved case and update customer fraud patterns.
        
        Args:
            case_data: The original case data (ticket, order, customer, etc.)
            verdict: The agent's verdict dict (predicted_action, refund_amount, reasoning)
        """
        case_id = case_data.get("case_id", "unknown")
        customer = case_data.get("customer", {})
        email = customer.get("email", "unknown")
        action = verdict.get("predicted_action", "")

        # Store case decision
        self.case_history[case_id] = {
            "case_id": case_id,
            "customer_email": email,
            "customer_name": customer.get("name", ""),
            "action": action,
            "refund_amount": verdict.get("refund_amount", 0.0),
            "reasoning": verdict.get("reasoning", ""),
            "was_fraud_flagged": any(kw in action for kw in ["FRAUD", "THEFT", "ESCALATE"]),
            "resolved_at": datetime.now().isoformat()
        }

        # Update per-customer fraud pattern tracking
        if email not in self.fraud_patterns:
            self.fraud_patterns[email] = {
                "customer_name": customer.get("name", ""),
                "total_cases": 0,
                "fraud_flags": 0,
                "escalations": 0,
                "total_refunded": 0.0,
                "case_ids": []
            }

        pattern = self.fraud_patterns[email]
        pattern["total_cases"] += 1
        pattern["case_ids"].append(case_id)
        pattern["total_refunded"] += verdict.get("refund_amount", 0.0)

        if "FRAUD" in action or "THEFT" in action:
            pattern["fraud_flags"] += 1
        if "ESCALATE" in action:
            pattern["escalations"] += 1

        self._save()

    def retrieve(self, customer_email: str) -> dict:
        """
        Retrieve past case history and fraud patterns for a customer.
        
        Args:
            customer_email: The customer's email address
        
        Returns:
            dict with past_cases list and fraud_pattern summary
        """
        past_cases = {
            cid: case for cid, case in self.case_history.items()
            if case.get("customer_email") == customer_email
        }

        fraud_pattern = self.fraud_patterns.get(customer_email, {})

        return {
            "customer_email": customer_email,
            "past_cases": past_cases,
            "fraud_pattern": fraud_pattern,
            "has_prior_history": len(past_cases) > 0,
            "has_prior_fraud_flags": fraud_pattern.get("fraud_flags", 0) > 0
        }

    def get_all_fraud_patterns(self) -> dict:
        """Return all tracked customer fraud patterns."""
        return self.fraud_patterns

    def clear(self):
        """Clear all memory (used for fresh evaluation runs)."""
        self.case_history = {}
        self.fraud_patterns = {}
        self._save()

    def summary(self) -> str:
        """Return a human-readable summary of memory contents."""
        total_cases = len(self.case_history)
        total_customers = len(self.fraud_patterns)
        flagged = sum(1 for p in self.fraud_patterns.values() if p.get("fraud_flags", 0) > 0)

        return (
            f"Memory Store: {total_cases} cases resolved, "
            f"{total_customers} unique customers tracked, "
            f"{flagged} customers flagged for fraud"
        )
