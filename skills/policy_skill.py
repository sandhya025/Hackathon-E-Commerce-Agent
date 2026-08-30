"""
Policy Skill — Store Policy Rule Matching Engine

Provides deterministic policy constraint verification functions:
- Return window (30-day) verification with date math
- VIP eligibility check (LTV >= $500 AND return rate < 5%)
- Final sale restriction detection
- Damage claim classification (item damaged vs. box-only damage)

Reference: data/store_policy.md (Apex Retail Customer Service & Refund Policy)
"""

from datetime import datetime, date


def check_return_window(delivery_date_str: str, current_date_str: str = None) -> dict:
    """
    Check if a return request falls within the 30-day return window.
    
    Policy Reference: Section 1 — Standard Items are eligible for return within 30 days of delivery.
    
    Args:
        delivery_date_str: Delivery date in YYYY-MM-DD format
        current_date_str: Current date override (defaults to today)
    
    Returns:
        dict with days_since_delivery, within_30_day_window, and status
    """
    if current_date_str is None:
        current_date_str = date.today().isoformat()

    delivery = datetime.strptime(delivery_date_str, "%Y-%m-%d").date()
    current = datetime.strptime(current_date_str, "%Y-%m-%d").date()
    days = (current - delivery).days

    within = days <= 30

    return {
        "delivery_date": delivery_date_str,
        "current_date": current_date_str,
        "days_since_delivery": days,
        "within_30_day_window": within,
        "status": "OPEN" if within else f"EXPIRED — {days} days since delivery ({days - 30} days past window)"
    }


def check_vip_eligibility(ltv: float, return_rate_pct: float) -> dict:
    """
    Check if a customer qualifies for VIP benefits.
    
    Policy Reference: Section 3 — VIP requires LTV >= $500.00 AND return rate < 5.0%.
    VIP Benefits: instant replacement/refund under $200 with zero return shipment, all fees waived.
    
    Args:
        ltv: Customer Lifetime Value in dollars
        return_rate_pct: Historical return rate percentage
    
    Returns:
        dict with qualification status and applicable benefits
    """
    ltv_ok = ltv >= 500.0
    rate_ok = return_rate_pct < 5.0
    is_vip = ltv_ok and rate_ok

    return {
        "ltv": ltv,
        "return_rate_pct": return_rate_pct,
        "ltv_meets_threshold": ltv_ok,
        "return_rate_below_threshold": rate_ok,
        "is_vip_qualified": is_vip,
        "benefits": {
            "instant_replacement_under_200": True,
            "waive_restocking_fees": True,
            "waive_return_shipping": True,
            "zero_return_shipment_under_200": True
        } if is_vip else {},
        "note": "VIP benefits active — instant 1-click replacement for damaged/lost items under $200" if is_vip else (
            "Not VIP qualified" + (": LTV below $500" if not ltv_ok else ": return rate >= 5%")
        )
    }


def check_final_sale(items: list) -> dict:
    """
    Check if any order items are marked as final sale.
    
    Policy Reference: Section 2 — Final sale items are non-refundable.
    Exception: Damaged/incorrect final-sale items receive Store Credit Only, never cash.
    
    Args:
        items: List of order item dicts with 'final_sale' boolean field
    
    Returns:
        dict with final sale status and refund restriction
    """
    fs_items = [item for item in items if item.get("final_sale", False)]
    has_fs = len(fs_items) > 0

    return {
        "has_final_sale_items": has_fs,
        "final_sale_item_names": [item.get("name") for item in fs_items],
        "refund_type_allowed": "STORE_CREDIT_ONLY" if has_fs else "STANDARD_REFUND",
        "policy_note": (
            "Final sale items are NON-REFUNDABLE. Exception: if damaged/incorrect, "
            "customer receives STORE CREDIT ONLY — never cash refund to original payment."
        ) if has_fs else "No final sale restrictions. Standard refund methods available."
    }


def analyze_damage_claim(photo_provided: bool, photo_verified_defect: bool, message: str) -> dict:
    """
    Classify the type of damage claim from the support ticket.
    
    Policy Reference: Section 4 —
    - Item damaged: Free replacement or 100% full refund (store credit if final sale)
    - Box damaged but product intact: 15% goodwill partial refund, no return required
    
    Args:
        photo_provided: Whether customer attached photo evidence
        photo_verified_defect: Whether the photo shows a verified defect on the ITEM
        message: The customer's support message text
    
    Returns:
        dict with damage classification and recommended policy action
    """
    msg = message.lower()

    # Detect "box/packaging damaged but item works fine" pattern
    box_keywords = ["box", "packaging", "carton", "outer", "shipping"]
    intact_keywords = ["fine", "works", "intact", "functional", "seems fine", "seems ok"]

    has_box_damage_mention = any(kw in msg for kw in box_keywords)
    has_intact_mention = any(kw in msg for kw in intact_keywords)

    item_damaged = photo_verified_defect
    box_damaged_only = has_box_damage_mention and has_intact_mention

    # If both are triggered, box_damaged_only takes priority (item works)
    if box_damaged_only:
        item_damaged = False

    if item_damaged:
        damage_type = "ITEM_DAMAGED"
    elif box_damaged_only:
        damage_type = "BOX_DAMAGED_ITEM_INTACT"
    else:
        damage_type = "NO_DAMAGE_CLAIMED"

    policy_actions = {
        "ITEM_DAMAGED": "Free replacement OR full refund (Store Credit if final sale). Photo evidence verified.",
        "BOX_DAMAGED_ITEM_INTACT": "15% goodwill partial refund, no return required. Product is functional.",
        "NO_DAMAGE_CLAIMED": "No damage claim — standard return policy applies."
    }

    return {
        "photo_evidence_provided": photo_provided,
        "photo_verified_defect": photo_verified_defect,
        "damage_type": damage_type,
        "recommended_action": policy_actions[damage_type]
    }
