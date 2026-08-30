"""
Fraud Skill — Fraud Risk Assessment Engine

Detects high-risk customer patterns:
- Serial return abuse (return rate >= 50% with > 3 orders)
- Wardrobing (buying items for one-time use and returning)
- Chargeback threats
- Coordinated fraud signals

Policy Reference: Section 5 — Serial Return Abuse threshold >= 50% across > 3 orders.
"""


def assess_fraud_risk(return_rate_pct: float, orders_count: int,
                      ticket_message: str = "", customer_email: str = "") -> dict:
    """
    Assess customer fraud risk based on return history and behavioral signals.
    
    Serial Return Abuse Rule (Section 5):
    - If historical return rate >= 50.0% across MORE than 3 lifetime orders
    → Flag for manual fraud review. No automatic refunds.
    
    Args:
        return_rate_pct: Customer's historical return rate percentage
        orders_count: Total lifetime order count
        ticket_message: The customer's support message (for behavior analysis)
        customer_email: Customer email for memory lookup
    
    Returns:
        dict with risk level, flags, and recommendation
    """
    # Serial returner check: rate >= 50% AND orders > 3
    is_serial_returner = return_rate_pct >= 50.0 and orders_count > 3

    # Wardrobing detection from message text
    msg = ticket_message.lower()
    wardrobing_signals = []
    if any(w in msg for w in ["wore", "worn", "wore it", "used it at"]):
        wardrobing_signals.append("Customer admitted wearing/using the item before returning")
    if any(w in msg for w in ["event", "party", "wedding", "prom", "gala", "dinner"]):
        wardrobing_signals.append("Item was used for a specific occasion/event")
    if "immediately" in msg or "right now" in msg:
        wardrobing_signals.append("Urgency in return request after event")

    # Chargeback threat detection
    chargeback_threat = any(w in msg for w in ["chargeback", "contact my bank", "dispute the charge", "credit card company"])

    # Composite risk score
    risk_score = 0
    risk_factors = []

    if is_serial_returner:
        risk_score += 50
        risk_factors.append(f"Serial returner: {return_rate_pct:.1f}% return rate across {orders_count} orders (threshold: >=50%, >3 orders)")
    elif return_rate_pct >= 30:
        risk_score += 15
        risk_factors.append(f"Elevated return rate: {return_rate_pct:.1f}%")

    if wardrobing_signals:
        risk_score += 30
        risk_factors.extend(wardrobing_signals)

    if chargeback_threat:
        risk_score += 10
        risk_factors.append("Chargeback threat detected in message")

    # Risk level classification
    if risk_score >= 50:
        risk_level = "HIGH"
    elif risk_score >= 20:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "return_rate_pct": return_rate_pct,
        "orders_count": orders_count,
        "is_serial_returner": is_serial_returner,
        "serial_returner_rule": "return_rate >= 50% AND orders > 3",
        "wardrobing_signals": wardrobing_signals,
        "chargeback_threat_detected": chargeback_threat,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "recommendation": (
            "ESCALATE_MANUAL_FRAUD_REVIEW — No automatic refunds for high-risk customers"
            if risk_level == "HIGH" else
            "PROCEED_WITH_CAUTION — Additional verification recommended"
            if risk_level == "MEDIUM" else
            "PROCEED_NORMALLY — No fraud signals detected"
        )
    }
