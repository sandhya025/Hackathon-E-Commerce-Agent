"""
Carrier Skill — Carrier Telemetry Analysis Engine

Analyzes carrier weight scale data, GPS delivery coordinates, and hub exception notes
to detect fraud (empty box claims), misdelivery, and internal carrier theft.

Policy Reference: Section 5 of Store Policy
- Weight Mismatch Rule: destination < 50% of origin OR delta > 1.0 lb → flag as fraud/theft
- GPS Mismatch: carrier delivered to wrong address → instant replacement
- Hub Tampering: re-taping or non-standard packaging at sorting hub → carrier theft
"""


def analyze_carrier_telemetry(origin_weight_lbs: float, destination_weight_lbs: float,
                               gps_match_address: bool, carrier_notes: str = "") -> dict:
    """
    Analyze carrier weight telemetry, GPS match, and hub notes.
    
    This is CRITICAL for detecting:
    1. Empty box fraud — customer claims empty box but weight data proves items were inside
    2. Internal carrier theft — weight drops dramatically at sorting hub
    3. Misdelivery — GPS coordinates don't match customer address
    
    Args:
        origin_weight_lbs: Weight at warehouse origin scan
        destination_weight_lbs: Weight at carrier delivery hub scale
        gps_match_address: Whether GPS coordinates match the delivery address
        carrier_notes: Exception notes from the carrier (e.g., re-taping, damage)
    
    Returns:
        dict with weight analysis, delivery integrity assessment, and flags
    """
    weight_delta = abs(origin_weight_lbs - destination_weight_lbs)
    ratio = destination_weight_lbs / origin_weight_lbs if origin_weight_lbs > 0 else 0.0

    # Weight Mismatch Rule: destination < 50% of origin OR delta > 1.0 lb
    is_weight_suspicious = weight_delta > 1.0 or ratio < 0.5

    # Detect tampering from carrier notes
    notes_lower = carrier_notes.lower()
    tampering_terms = ["re-taped", "re-tape", "non-standard", "security tape",
                       "tampered", "cut open", "yellow tape", "re-sealed"]
    has_tampering = any(term in notes_lower for term in tampering_terms)

    # Build flags list
    flags = []
    if is_weight_suspicious:
        flags.append(
            f"CRITICAL WEIGHT ANOMALY: Origin {origin_weight_lbs} lbs → "
            f"Destination {destination_weight_lbs} lbs (Δ {weight_delta:.2f} lbs, "
            f"ratio {ratio:.1%})"
        )
    if has_tampering:
        flags.append(f"TAMPERING DETECTED: Carrier notes indicate '{carrier_notes}'")
    if not gps_match_address:
        flags.append("GPS MISMATCH: Package delivered to incorrect address")

    # Determine delivery integrity verdict
    if is_weight_suspicious and has_tampering:
        integrity = "CARRIER_TRANSIT_THEFT"
        summary = (
            "Major weight discrepancy with physical tampering evidence. "
            "Package was likely opened and contents removed at carrier sorting hub."
        )
    elif is_weight_suspicious:
        integrity = "WEIGHT_ANOMALY_FRAUD_SUSPECTED"
        summary = (
            f"Carrier weight data proves package was delivered at near-origin weight "
            f"({destination_weight_lbs} lbs vs {origin_weight_lbs} lbs, "
            f"delta only {weight_delta:.2f} lbs). "
            f"An empty box claim is NOT credible."
            if weight_delta <= 1.0 and ratio >= 0.5
            else f"Significant weight discrepancy detected ({weight_delta:.2f} lbs). "
                 f"Investigate for potential fraud."
        )
    elif not gps_match_address:
        integrity = "CARRIER_MISDELIVERY"
        summary = (
            "GPS coordinates confirm carrier delivered package to a different address. "
            "This is a carrier error — customer should receive immediate replacement."
        )
    else:
        integrity = "DELIVERY_VERIFIED_NORMAL"
        summary = (
            f"Delivery verified: weight matches ({origin_weight_lbs} → "
            f"{destination_weight_lbs} lbs, Δ {weight_delta:.2f}), "
            f"GPS confirmed at correct address."
        )

    return {
        "origin_weight_lbs": origin_weight_lbs,
        "destination_weight_lbs": destination_weight_lbs,
        "weight_delta_lbs": round(weight_delta, 2),
        "destination_to_origin_ratio": round(ratio, 4),
        "is_weight_suspicious": is_weight_suspicious,
        "gps_match_address": gps_match_address,
        "has_tampering_indicators": has_tampering,
        "carrier_notes": carrier_notes,
        "delivery_integrity": integrity,
        "summary": summary,
        "flags": flags
    }
