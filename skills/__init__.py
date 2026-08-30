"""
Skills Module — Specialized Deterministic Tools for Dispute Resolution Agent.

Each skill encapsulates domain expertise as callable tool functions:
- policy_skill: Store policy rule matching and constraint verification
- carrier_skill: Carrier weight telemetry and GPS analysis
- fraud_skill: Fraud risk scoring and pattern detection
- financial_skill: Deterministic financial calculator (fees, promos, refunds)
"""

from skills.policy_skill import check_return_window, check_vip_eligibility, check_final_sale, analyze_damage_claim
from skills.carrier_skill import analyze_carrier_telemetry
from skills.fraud_skill import assess_fraud_risk
from skills.financial_skill import calculate_refund
