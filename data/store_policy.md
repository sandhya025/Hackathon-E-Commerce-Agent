# Apex Retail - Customer Service & Refund Policy

This document defines the binding rules and thresholds for customer support agents handling returns, refunds, damages, and carrier disputes.

---

## 1. Standard Return & Refund Windows
- **Standard Items**: Eligible for return within **30 days** of delivery date.
- **Return Shipping**: Free for Apparel and Shoes. $5.99 flat deduction for all other categories unless the item was damaged/defective on arrival.
- **Restocking Fee**:
  - **Electronics**: $15.00 restocking fee if opened/unboxed (waived if defective).
  - **Other Categories**: $0.00 restocking fee.

---

## 2. Special Item Exclusions & Final Sale
- **Final Sale Items**: Items marked with `final_sale: true` or purchased during clearance events (>50% discount) are **non-refundable**.
  - *Exception*: If a final-sale item arrives damaged or incorrect, the customer is eligible for **Store Credit Only**, never cash to the original payment method.
- **Digital Goods & Gift Cards**: Strictly non-refundable under all circumstances.

---

## 3. VIP / High-LTV Customer Exemption
- **VIP Qualification**: Customer Lifetime Value (LTV) **>= $500.00** AND historical Return Rate **< 5.0%**.
- **VIP Benefit**: 
  - Instant replacement or refund approved with **zero return shipment required** on damaged/lost claims under $200.00.
  - Waive all restocking and return shipping fees.

---

## 4. Damaged in Transit & Defective Claims
- If an item arrives damaged:
  - Customer must provide photo evidence of damage.
  - Customer receives choice of **Free Immediate Replacement** or **100% Full Refund**.
  - If package packaging is damaged but the product inside is intact and functional: Offer a **15% goodwill partial refund**, no return required.

---

## 5. Lost in Transit, Delivery Disputes & Fraud Protection
- **Carrier Weight Telemetry Check**:
  - Compare `origin_scan_weight_lbs` (warehouse scale) vs. `destination_scale_weight_lbs` (carrier delivery hub scale).
  - **Weight Mismatch Rule**: If destination scale weight is **< 50% of origin weight** or delta > **1.0 lb**, flag as **Carrier Theft / Empty Box Fraud**.
  - *Action*: **DO NOT refund immediately**. Escalate to Carrier Claims & Security.
- **Porch Piracy / Non-Receipt with "Delivered" Status**:
  - If carrier GPS coordinates match the delivery address: File a carrier claim, require customer signature verification for replacement.
  - If carrier GPS coordinates **do not match** delivery address (misdelivered by carrier): Issue **Instant Replacement** immediately.
- **Serial Return Abuse**:
  - If customer historical Return Rate **>= 50.0%** across more than 3 lifetime orders: Flag for manual fraud review. No automatic refunds.

---

## 6. Partial Returns with Promotional Discounts
- When returning part of a "Buy More, Save More" or bundle discount order, the refund amount must be recalculated based on the remaining retained items. The discount is revoked if retained items fall below the promotional threshold.
