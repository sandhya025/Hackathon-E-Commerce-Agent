"""
Financial Skill — Deterministic Financial Calculator

Precise refund amount calculations with:
- Restocking fees ($15 for opened electronics, waived if defective or VIP)
- Return shipping deductions ($5.99 for non-Apparel/Shoes, waived if defective)
- Promotional discount clawback (recalculate when returning part of a bundle)
- Goodwill partial refunds (15% for damaged box with intact product)
- Store credit calculations (for damaged final-sale items)

This eliminates financial hallucinations — all math is deterministic.
"""


def calculate_refund(calculation_type: str, item_price: float = 0.0,
                     total_paid: float = 0.0, category: str = "",
                     is_opened: bool = False, is_defective: bool = False,
                     is_final_sale: bool = False, promo_discount: float = 0.0,
                     items_kept_value: float = 0.0, is_vip: bool = False) -> dict:
    """
    Calculate the exact refund amount based on the scenario type.
    
    Calculation Types:
    - no_refund: $0 (fraud, expired window, escalations)
    - replacement: $0 monetary (free replacement shipped instead)
    - store_credit: total_paid as store credit (damaged final sale, Section 2)
    - goodwill_partial: 15% of item_price (damaged box, intact item, Section 4)
    - standard_return_with_fees: item_price - restocking - return_shipping (Section 1)
    - promotional_clawback: total_paid - items_kept_value (Section 6)
    
    Args:
        calculation_type: The type of refund calculation to perform
        item_price: Individual item price for the returned item
        total_paid: Total amount the customer originally paid
        category: Product category (Electronics, Apparel, Shoes, Home, etc.)
        is_opened: Whether the item was opened/used
        is_defective: Whether the item is defective/damaged
        is_final_sale: Whether the item is a final sale item
        promo_discount: Promotional discount that was applied to the order
        items_kept_value: Total full price of items the customer is keeping
        is_vip: Whether the customer has VIP status (for fee waivers)
    
    Returns:
        dict with exact refund_amount, breakdown, and all fee details
    """
    result = {
        "calculation_type": calculation_type,
        "inputs": {
            "item_price": item_price,
            "total_paid": total_paid,
            "category": category,
            "is_opened": is_opened,
            "is_defective": is_defective,
            "is_final_sale": is_final_sale,
            "promo_discount": promo_discount,
            "items_kept_value": items_kept_value,
            "is_vip": is_vip
        }
    }

    if calculation_type == "no_refund":
        result["refund_amount"] = 0.00
        result["breakdown"] = "No refund applicable (fraud/expired/escalation)."

    elif calculation_type == "replacement":
        result["refund_amount"] = 0.00
        result["breakdown"] = "Free replacement shipped — no monetary refund issued."

    elif calculation_type == "store_credit":
        credit = round(total_paid, 2)
        result["refund_amount"] = credit
        result["payment_method"] = "STORE_CREDIT_ONLY"
        result["breakdown"] = (
            f"Store credit of ${credit:.2f} issued. "
            f"Final sale item — cash refund to original payment method is NOT allowed per Section 2."
        )

    elif calculation_type == "goodwill_partial":
        refund = round(item_price * 0.15, 2)
        result["refund_amount"] = refund
        result["goodwill_percentage"] = 15
        result["breakdown"] = (
            f"15% goodwill partial refund per Section 4: "
            f"15% × ${item_price:.2f} = ${refund:.2f}. "
            f"No return required — product is functional."
        )

    elif calculation_type == "standard_return_with_fees":
        # Restocking fee: $15 for opened Electronics, waived if defective or VIP
        if category == "Electronics" and is_opened and not is_defective and not is_vip:
            restocking_fee = 15.00
        else:
            restocking_fee = 0.00

        # Return shipping: free for Apparel/Shoes, $5.99 for others
        # Waived if defective or VIP
        if is_defective or is_vip:
            return_shipping = 0.00
        elif category in ["Apparel", "Shoes"]:
            return_shipping = 0.00
        else:
            return_shipping = 5.99

        net_refund = round(max(0.0, item_price - restocking_fee - return_shipping), 2)

        result["restocking_fee"] = restocking_fee
        result["return_shipping_deduction"] = return_shipping
        result["refund_amount"] = net_refund
        result["return_required"] = True
        result["breakdown"] = (
            f"Item price: ${item_price:.2f}\n"
            f"  − Restocking fee: ${restocking_fee:.2f}"
            f"{' (Electronics, opened, non-defective)' if restocking_fee > 0 else ' (waived)'}\n"
            f"  − Return shipping: ${return_shipping:.2f}"
            f"{' (non-Apparel/Shoes category)' if return_shipping > 0 else ' (free for ' + category + ')'}\n"
            f"  = Net refund: ${net_refund:.2f}"
        )

    elif calculation_type == "promotional_clawback":
        # When returning items from a promo bundle, discount is revoked
        # Customer now owes full price for kept items
        # Refund = total_paid - kept_items_full_price
        new_owed = items_kept_value
        refund = round(max(0.0, total_paid - new_owed), 2)

        result["original_paid"] = total_paid
        result["kept_items_full_price"] = items_kept_value
        result["promo_discount_clawed_back"] = promo_discount
        result["refund_amount"] = refund
        result["return_required"] = True
        result["breakdown"] = (
            f"Original paid: ${total_paid:.2f} (with ${promo_discount:.2f} promo discount)\n"
            f"Returning item(s) breaks promotional threshold.\n"
            f"Kept items at full price: ${items_kept_value:.2f}\n"
            f"Promo discount CLAWED BACK per Section 6.\n"
            f"Refund = ${total_paid:.2f} − ${items_kept_value:.2f} = ${refund:.2f}"
        )

    else:
        result["refund_amount"] = 0.00
        result["breakdown"] = f"Unknown calculation type: {calculation_type}"

    return result
