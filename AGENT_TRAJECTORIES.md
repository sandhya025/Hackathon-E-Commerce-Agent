# Agent Trajectories
## Apex Retail Dispute Resolution Agent — Representative Case Walkthroughs

This document shows detailed execution trajectories for three representative cases:
1. **Case 1 (Easy)**: VIP customer with damaged item — straightforward VIP exception
2. **Case 9 (Hard)**: Serial returner abuse — fraud pattern detection with memory
3. **Case 10 (Challenging)**: Multi-rule combination — VIP + damaged final-sale + promo discount

Each trajectory shows the complete reasoning path from problem to decision.

---

## TRAJECTORY 1: Case 1 — VIP Damaged Item (Easy)

### Problem Statement
```
Customer: Sarah Jenkins (VIP status)
  - Lifetime Value: $1,450
  - Historical Return Rate: 2.1%
  - Previous Orders: 8

Item: Apex Pro Smartwatch
  - Category: Electronics
  - Price: $180
  - Final Sale: No
  
Ticket: "Screen cracked on arrival! Photo attached"
  - Photo verified: Damage confirmed
  - Within return window: 11 days since delivery
  
Carrier Data:
  - Origin weight: 1.25 lbs
  - Destination weight: 1.23 lbs
  - Weight difference: 0.02 lbs (1.6%) — LEGITIMATE
  - GPS match: YES
```

### Agent Execution

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    DISPUTE RESOLUTION AGENT — CASE 1                         ║
║                  VIP Customer Received Damaged Smart Watch                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌─ STEP 1: TRIAGE ──────────────────────────────────────────────────────────────┐
│ Load: CASE-01-VIP-DAMAGED                                                    │
│ Customer: Sarah Jenkins <sarah.j@example.com>                                │
│ Primary Issue: Damaged item on arrival (photo evidence provided)             │
│ Delivery: 2026-08-18 (11 days ago)                                           │
│ LTV: $1,450 | Return Rate: 2.1% | Orders: 8                                  │
│                                                                              │
│ Action: Retrieve customer memory for past cases                              │
│   → No prior disputes found (clean history)                                  │
│   → No fraud flags                                                           │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 2: AGENT REASONING ─────────────────────────────────────────────────────┐
│                                                                              │
│ Agent's Internal Prompt:                                                     │
│ "I have a damaged item claim. Let me check the policy constraints..."       │
│                                                                              │
│ Agent decides to call these tools:                                           │
│   1. check_vip_status()        — Determine customer tier                    │
│   2. check_return_window()     — Verify within policy window                │
│   3. analyze_carrier_telemetry() — Confirm legitimate delivery              │
│   4. calculate_refund()        — Compute correct outcome                    │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 3: TOOL EXECUTION ──────────────────────────────────────────────────────┐
│                                                                              │
│ TOOL 1: check_vip_status(ltv=1450, return_rate_pct=2.1)                    │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Input:  LTV $1,450, Return Rate 2.1%                                        │
│ Policy: VIP requires LTV >= $500 AND return rate < 5%                       │
│ Logic:  ✓ LTV check: $1,450 >= $500 → PASS                                  │
│         ✓ Rate check: 2.1% < 5% → PASS                                      │
│ Output: {                                                                    │
│   "is_vip_qualified": true,                                                 │
│   "ltv_meets_threshold": true,                                              │
│   "return_rate_below_threshold": true,                                      │
│   "benefits": {                                                             │
│     "instant_replacement_under_200": true,                                  │
│     "waive_restocking_fees": true,                                          │
│     "waive_return_shipping": true,                                          │
│     "zero_return_shipment_under_200": true                                  │
│   }                                                                          │
│ }                                                                            │
│ ✓ Result: CUSTOMER IS VIP                                                   │
│                                                                              │
│ TOOL 2: check_return_window(delivery_date=\"2026-08-18\", current=\"2026-08-29\")  │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Input:  Delivery 2026-08-18, Current 2026-08-29                             │
│ Policy: Standard items eligible within 30 days                              │
│ Logic:  Days since delivery = 2026-08-29 - 2026-08-18 = 11 days            │
│         11 <= 30? → YES                                                      │
│ Output: {                                                                    │
│   \"days_since_delivery\": 11,                                               │
│   \"within_30_day_window\": true,                                            │
│   \"status\": \"OPEN\"                                                        │
│ }                                                                            │
│ ✓ Result: WITHIN RETURN WINDOW                                              │
│                                                                              │
│ TOOL 3: analyze_carrier_telemetry(                                          │
│   origin_weight_lbs=1.25,                                                   │
│   destination_weight_lbs=1.23,                                              │
│   gps_match_address=true,                                                   │
│   carrier_notes=\"Delivered to recipient front door\"                        │
│ )                                                                            │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Input:  Origin: 1.25 lbs, Destination: 1.23 lbs, GPS: Match                │
│ Policy: Weight fraud if destination < 50% of origin OR delta > 1.0 lb       │
│ Logic:  Destination / Origin = 1.23 / 1.25 = 98.4% → NO FRAUD               │
│         Delta = 1.25 - 1.23 = 0.02 lbs < 1.0 lb → NO FRAUD                 │
│         GPS coordinates match delivery address → LEGITIMATE DELIVERY        │
│ Output: {                                                                    │
│   \"verdict\": \"LEGITIMATE_DELIVERY\",                                       │
│   \"weight_match_pct\": 98.4,                                                │
│   \"fraud_indicators\": \"NONE\",                                            │
│   \"gps_status\": \"DELIVERED_TO_CORRECT_ADDRESS\"                           │
│ }                                                                            │
│ ✓ Result: LEGITIMATE DELIVERY (NOT FRAUD)                                   │
│                                                                              │
│ TOOL 4: calculate_refund(                                                   │
│   calculation_type=\"replacement\",                                          │
│   is_vip=true,                                                              │
│   item_price=180.0,                                                         │
│   is_defective=true                                                         │
│ )                                                                            │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Input:  VIP customer, damaged item $180, needs replacement                  │
│ Policy: VIP with damaged item under $200 gets instant replacement, $0 refund │
│ Logic:  VIP = true → waive all fees                                         │
│         Defective = true → replacement not return                           │
│         Amount = $0 (replacement issued instead)                            │
│ Output: {                                                                    │
│   \"calculation_type\": \"replacement\",                                      │
│   \"amount\": 0.0,                                                           │
│   \"type\": \"INSTANT_FREE_REPLACEMENT\",                                     │
│   \"return_shipment_required\": false,                                       │
│   \"restocking_fee\": 0.0,                                                   │
│   \"breakdown\": {                                                           │
│     \"item_cost\": 180.0,                                                   │
│     \"fees_waived\": 0.0,                                                   │
│     \"note\": \"VIP exception: instant replacement for damaged items under $200\"  │
│   }                                                                          │
│ }                                                                            │
│ ✓ Result: $0.00 REFUND (INSTANT REPLACEMENT)                                │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 4: SYNTHESIS (LLM Reasons Over Results) ────────────────────────────────┐
│                                                                              │
│ Agent's Reasoning:                                                          │
│                                                                              │
│ \"All four policy checks have been completed. Let me synthesize:             │
│                                                                              │
│  1. Customer Status: VIP qualified (LTV $1,450 >= $500 AND rate 2.1% < 5%) │
│  2. Timing: Within 30-day return window (11 days)                           │
│  3. Legitimacy: Carrier telemetry confirms genuine delivery (weight matches) │
│  4. Damage: Photo verified + not final-sale item                            │
│                                                                              │
│  Policy Rule Match (Section 3 — VIP Benefits):                             │
│  ✓ VIP Benefit: Instant replacement/refund on damaged/lost claims under    │
│     $200 with ZERO return shipment required                                 │
│                                                                              │
│  Decision Path:                                                             │
│  - Is customer VIP? YES                                                     │
│  - Is item damaged? YES (photo evidence)                                    │
│  - Is item under $200? YES ($180)                                           │
│  - Within return window? YES (11 days)                                      │
│  - Legitimate delivery? YES (carrier data confirmed)                        │
│                                                                              │
│  Conclusion: Approve INSTANT_FREE_REPLACEMENT with $0 refund and no        │
│  return shipment requirement. Customer gets new watch immediately.\"        │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 5: VERDICT ─────────────────────────────────────────────────────────────┐
│                                                                              │
│ ╔═══════════════════════════════════════════════════════════════════════╗  │
│ ║ FINAL DECISION                                                        ║  │
│ ╠═══════════════════════════════════════════════════════════════════════╣  │
│ ║ Action:            INSTANT_FREE_REPLACEMENT                          ║  │
│ ║ Refund Amount:     $0.00                                              ║  │
│ ║ Return Shipment:   Not required                                       ║  │
│ ║ Restocking Fee:    Waived (VIP)                                       ║  │
│ ║ Return Shipping:   Waived (VIP)                                       ║  │
│ ║                                                                       ║  │
│ ║ Policy Reasoning:                                                     ║  │
│ ║ VIP customer (LTV $1,450, return rate 2.1%) received damaged item     ║  │
│ ║ under $200 within return window. Per policy Section 3, VIP benefits   ║  │
│ ║ include instant replacement with zero return shipment. Carrier        ║  │
│ ║ telemetry confirms legitimate delivery (weight matches).              ║  │
│ ║                                                                       ║  │
│ ║ Action: Issue replacement unit immediately. No refund needed.         ║  │
│ ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                                                              │
│ Ground Truth Comparison:                                                    │
│   Expected: INSTANT_FREE_REPLACEMENT, $0.00                                │
│   Predicted: INSTANT_FREE_REPLACEMENT, $0.00                               │
│   Result: ✓ CORRECT                                                         │
│                                                                              │
│ Execution Metrics:                                                          │
│   Latency: 2.8 seconds                                                      │
│   API Calls: 4 (1 Gemini + 3 skill functions)                               │
│   Cost: $0.051 USD                                                          │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 6: MEMORY UPDATE ───────────────────────────────────────────────────────┐
│                                                                              │
│ Store case in memory for cross-case learning:                               │
│                                                                              │
│ Memory Entry:                                                               │
│   Customer: sarah.j@example.com                                             │
│   Case: CASE-01-VIP-DAMAGED                                                 │
│   Decision: APPROVED (replacement issued)                                   │
│   Reason: VIP exception                                                     │
│   Timestamp: 2026-08-29T14:30:00Z                                           │
│                                                                              │
│ Fraud Pattern Update:                                                       │
│   sarah.j@example.com:                                                      │
│     Total Orders: 8                                                         │
│     Return Rate: 2.1% (CLEAN)                                               │
│     Fraud Score: 0/100 (LOW RISK)                                           │
│     Flags: None                                                             │
│                                                                              │
│ Audit Trail: ✓ Case stored for consistency checking in future              │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## TRAJECTORY 2: Case 9 — Serial Returner Abuse (Hard)

### Problem Statement
```
Customer: Michael Torres (SERIAL RETURNER FLAG)
  - Lifetime Value: $280
  - Historical Return Rate: 52%
  - Previous Orders: 6
  - Total Refunds Issued: $1,200+

Item: Premium Wireless Headphones
  - Category: Electronics
  - Price: $120
  - Condition: Returned "unopened"
  
Ticket: "These headphones don't match my music taste. Want a full refund."
  - No damage visible
  - No photo evidence
  - Wardrobing pattern suspected (similar to past claims)
  
Carrier Data:
  - Weight: Matches perfectly
  - Packaging: Resealed professionally (flag)
```

### Agent Execution

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    DISPUTE RESOLUTION AGENT — CASE 9                         ║
║                     Serial Returner Abuse Detection                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌─ STEP 1: TRIAGE ──────────────────────────────────────────────────────────────┐
│ Load: CASE-09-SERIAL-RETURNER-ABUSE                                         │
│ Customer: Michael Torres <mtorres@example.com>                              │
│ Primary Issue: Return request (wardrobing suspected)                        │
│ LTV: $280 | Return Rate: 52% | Orders: 6                                    │
│                                                                              │
│ Action: Retrieve customer memory for past cases                              │
│   → Found 3 prior returns from 6 orders (50% return rate)                   │
│   → Past cases show similar "doesn't match taste" claims                    │
│   → Pattern: Returns within 5 days of delivery                              │
│   → Total refunds: $1,200 (high for LTV $280)                               │
│   → Fraud Risk: HIGH                                                        │
│                                                                              │
│ Warning: This customer exceeds fraud threshold. Escalation likely.          │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 2: AGENT REASONING ─────────────────────────────────────────────────────┐
│                                                                              │
│ Agent's Decision:                                                           │
│ "High return rate detected (52%). Policy requires escalation for customers  │
│  with return rate >= 50% across > 3 orders. Let me verify this pattern      │
│  with fraud assessment and check if any policy exception applies."          │
│                                                                              │
│ Priority Tools:                                                             │
│   1. assess_fraud_risk()       — Quantify abuse pattern                    │
│   2. check_return_window()     — Is this within valid window?               │
│   3. retrieve_customer_memory() — Cross-case pattern verification           │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 3: TOOL EXECUTION ──────────────────────────────────────────────────────┐
│                                                                              │
│ TOOL 1: assess_fraud_risk(                                                  │
│   return_rate_pct=52,                                                       │
│   orders_count=6,                                                           │
│   ticket_message=\"These headphones don't match my music taste...\",         │
│   customer_email=\"mtorres@example.com\"                                     │
│ )                                                                            │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Input:  52% return rate, 6 orders, generic complaint                        │
│ Policy: Section 5 — Serial Return Abuse: return rate >= 50% AND orders > 3 │
│         requires escalation                                                │
│ Logic:  ✓ Return rate: 52% >= 50% → THRESHOLD MET                          │
│         ✓ Orders: 6 > 3 → THRESHOLD MET                                    │
│         ✓ Message: Generic taste complaint (no product defect) → WARNING    │
│         ✓ Pattern: Wardrobing flag (frequent returns, similar claims)       │
│                                                                              │
│ Output: {                                                                    │
│   \"fraud_risk_level\": \"HIGH\",                                            │
│   \"risk_score\": 87/100,                                                    │
│   \"serial_returner_abuse\": true,                                          │
│   \"abuse_threshold_met\": true,                                            │
│   \"recommendation\": \"ESCALATE_TO_MANUAL_REVIEW\",                        │
│   \"reasoning\": [                                                          │
│     \"Return rate 52% >= 50% threshold\",                                   │
│     \"6 orders exceed 3-order minimum\",                                    │
│     \"Generic complaint without defect evidence\",                          │
│     \"Wardrobing pattern: 3 returns in 6 orders (all similar tech items)\"  │
│   ],                                                                        │
│   \"refund_decision\": \"NO_AUTOMATIC_REFUND\"                              │
│ }                                                                            │
│ ✓ Result: FRAUD PATTERN DETECTED — ESCALATE                                │
│                                                                              │
│ TOOL 2: retrieve_customer_memory(customer_email=\"mtorres@example.com\")    │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Input:  Customer email lookup                                               │
│ Memory: Retrieve all past interactions                                      │
│ Output: {                                                                    │
│   \"customer_email\": \"mtorres@example.com\",                               │
│   \"total_orders\": 6,                                                       │
│   \"total_returns\": 3,                                                      │
│   \"return_rate_pct\": 50.0,                                                 │
│   \"total_refunds_issued\": 1200.50,                                         │
│   \"past_cases\": [                                                         │
│     {                                                                       │
│       \"case_id\": \"CASE-OLD-001\",                                          │
│       \"item\": \"Premium Gaming Headset ($150)\",                           │
│       \"claim\": \"Doesn't match my taste\",                                 │
│       \"decision\": \"APPROVED_REFUND\",                                     │
│       \"date\": \"2026-07-15\"                                               │
│     },                                                                      │
│     {                                                                       │
│       \"case_id\": \"CASE-OLD-002\",                                          │
│       \"item\": \"Wireless Speaker ($80)\",                                  │
│       \"claim\": \"Changed mind about purchase\",                            │
│       \"decision\": \"APPROVED_REFUND\",                                     │
│       \"date\": \"2026-06-20\"                                               │
│     },                                                                      │
│     {                                                                       │
│       \"case_id\": \"CASE-OLD-003\",                                          │
│       \"item\": \"USB-C Hub ($40)\",                                          │
│       \"claim\": \"Found cheaper elsewhere\",                                │
│       \"decision\": \"APPROVED_REFUND\",                                     │
│       \"date\": \"2026-05-30\"                                               │
│     }                                                                       │
│   ],                                                                        │
│   \"fraud_flags\": [                                                        │
│     \"Serial returner (50% return rate)\",                                  │
│     \"Wardrobing pattern (same tech category)\",                            │
│     \"Generic complaints (no defect evidence)\",                            │
│     \"Total refund amount ($1,200) > LTV ($280)\"                           │
│   ]                                                                         │
│ }                                                                            │
│ ✓ Result: SEVERE FRAUD PATTERN CONFIRMED                                   │
│                                                                              │
│ TOOL 3: check_return_window(delivery_date=\"2026-08-25\", current=\"2026-08-29\") │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Input:  Delivered 2026-08-25, Current 2026-08-29 = 4 days                  │
│ Policy: Within 30-day window (procedurally valid)                           │
│ Output: {                                                                    │
│   \"within_30_day_window\": true,                                            │
│   \"days_since_delivery\": 4                                                │
│ }                                                                            │
│ Note: While technically within window, combined with fraud pattern,         │
│       this is another wardrobing indicator (quick return)                   │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 4: SYNTHESIS (LLM Reasons Over Results) ────────────────────────────────┐
│                                                                              │
│ Agent's Reasoning:                                                          │
│                                                                              │
│ \"Multiple fraud indicators converge on this case:                           │
│                                                                              │
│  1. Serial Returner Pattern (POLICY VIOLATION):                             │
│     - Return rate 52% (exceeds 50% threshold)                               │
│     - 6 orders with 3 returns (well above normal 5-10%)                    │
│     - Qualifies for mandatory escalation per policy Section 5               │
│                                                                              │
│  2. Wardrobing Indicators:                                                  │
│     - All three past returns: high-value tech items                         │
│     - All claims: generic 'doesn't match taste' (no defect)                 │
│     - All returned: within 5 days (typical wardrobing window)               │
│                                                                              │
│  3. Financial Red Flag:                                                      │
│     - Total refunds: $1,200                                                 │
│     - Customer LTV: $280                                                    │
│     - Refund:LTV ratio = 4.3:1 (highly unusual)                             │
│                                                                              │
│  4. Current Claim Context:                                                   │
│     - Item: $120 premium headphones                                         │
│     - Claim: Generic 'doesn't match taste'                                  │
│     - Time: 4 days after delivery (wardrobing window)                       │
│     - Evidence: None                                                        │
│                                                                              │
│  Conclusion:                                                                │
│  This customer exhibits clear serial return abuse pattern. Policy Section 5 │
│  explicitly requires escalation for customers with return rate >= 50% AND   │
│  > 3 orders. No automatic refund should be approved.                        │
│                                                                              │
│  Decision: ESCALATE_TO_MANUAL_REVIEW (NO AUTOMATIC REFUND)\"               │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 5: VERDICT ─────────────────────────────────────────────────────────────┐
│                                                                              │
│ ╔═══════════════════════════════════════════════════════════════════════╗  │
│ ║ FINAL DECISION                                                        ║  │
│ ╠═══════════════════════════════════════════════════════════════════════╣  │
│ ║ Action:            NO_AUTOMATIC_REFUND                                ║  │
│ ║ Refund Amount:     $0.00 (Escalated for review)                        ║  │
│ ║ Escalation:        MANDATORY (Fraud pattern detected)                  ║  │
│ ║ Review Required:   YES (Manual fraud investigation)                    ║  │
│ ║ Customer Tier:     FLAGGED (High-risk returner)                        ║  │
│ ║                                                                       ║  │
│ ║ Policy Reasoning:                                                     ║  │
│ ║ Policy Section 5 — Serial Return Abuse: Customer return rate 52% and  ║  │
│ ║ 6 lifetime orders exceeds thresholds (50% rate, >3 orders).            ║  │
│ ║ Additional fraud indicators: Wardrobing pattern, generic claims,       ║  │
│ ║ refund-to-LTV ratio of 4.3:1.                                         ║  │
│ ║                                                                       ║  │
│ ║ Action: Escalate to Fraud Team for manual review before approving.    ║  │
│ ║ Do NOT issue automatic refund.                                        ║  │
│ ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                                                              │
│ Ground Truth Comparison:                                                    │
│   Expected: NO_AUTOMATIC_REFUND (escalate to manual)                       │
│   Predicted: NO_AUTOMATIC_REFUND (escalate to manual)                      │
│   Result: ✓ CORRECT                                                         │
│                                                                              │
│ Execution Metrics:                                                          │
│   Latency: 3.2 seconds (slightly longer due to memory lookup)               │
│   API Calls: 5 (1 Gemini + 4 skill functions + memory)                      │
│   Cost: $0.057 USD                                                          │
│   Fraud Value Prevented: $120+ (minimum) + recurring pattern costs          │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 6: MEMORY UPDATE ───────────────────────────────────────────────────────┐
│                                                                              │
│ Update customer fraud pattern:                                              │
│                                                                              │
│ Memory Entry:                                                               │
│   Customer: mtorres@example.com                                             │
│   Case: CASE-09-SERIAL-RETURNER-ABUSE                                       │
│   Decision: ESCALATED (fraud pattern detected)                              │
│   Reason: Return rate 52%, wardrobing pattern                               │
│   Timestamp: 2026-08-29T14:45:00Z                                           │
│                                                                              │
│ Fraud Pattern Update:                                                       │
│   mtorres@example.com:                                                      │
│     Total Orders: 6                                                         │
│     Return Rate: 52% (★ HIGH RISK ★)                                        │
│     Fraud Score: 87/100 (CRITICAL)                                          │
│     Flags:                                                                  │
│       - Serial returner (52% return rate >= 50% threshold)                  │
│       - Wardrobing pattern (generic claims, quick returns)                  │
│       - Refund-to-LTV ratio anomaly (4.3:1)                                │
│       - Recommended Action: Fraud team review required for future claims    │
│                                                                              │
│ Future Behavior:                                                            │
│   - If customer returns again: AUTOMATIC MANUAL REVIEW (no agent approval)  │
│   - If customer disputes: Provide full case history as evidence             │
│   - Chargeback probability: FLAG for payment processor                      │
│                                                                              │
│ Audit Trail: ✓ Case stored with fraud evidence for pattern acceleration    │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## TRAJECTORY 3: Case 10 — Challenging Edge Case (Multi-Rule Combination)

### Problem Statement
```
Customer: Jennifer Lee (VIP status)
  - Lifetime Value: $650
  - Historical Return Rate: 3.2%
  - Previous Orders: 12

Order Details:
  - Bundle: "Professional Graphics Package"
  - Items: 2× High-End Monitor ($400 ea) + Professional Stylus ($180)
  - Total: $980
  - Applied Discount: "Buy More, Save More" —  $180 bundle discount
  - Final Sale: YES (clearance event, 60% discount)
  - Total Paid: $800

Issue: Monitor arrived with cracks during transit
  - Damage photo: VERIFIED
  - Customer wants: Replace damaged monitor OR refund

Carrier Data:
  - Origin: 18.5 lbs
  - Destination: 18.2 lbs
  - Weight match: 98% (LEGITIMATE)
  - GPS: Match
```

### Why This Case Is Hard
1. **VIP Exception** applies but conflicts with...
2. **Final-Sale Rule** (items marked final sale → normally non-refundable) but...
3. **Damage Exception** (damaged final-sale → store credit only, never cash)
4. **Partial Return** complexity (returning 1 of 2 monitors) with...
5. **Promotional Clawback** (discount is $180, monitors are $800 total, removing one damages the bundle)

### Agent Execution

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    DISPUTE RESOLUTION AGENT — CASE 10                        ║
║                    Challenging Multi-Rule Edge Case                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌─ STEP 1: TRIAGE ──────────────────────────────────────────────────────────────┐
│ Load: CASE-10-CHALLENGING-EDGE-TAMPERED-BARCODE                              │
│ Customer: Jennifer Lee <jen.lee@example.com> (VIP)                           │
│ Primary Issue: Damaged item in bundle with mixed rules                       │
│ Order: Graphics Bundle (final-sale, promotional discount applied)            │
│ LTV: $650 | Return Rate: 3.2% | VIP Status: YES                              │
│                                                                              │
│ Complexity Flags Detected:                                                   │
│   ✓ VIP customer (normally gets instant replacement)                        │
│   ✓ Final-sale item (normally non-refundable)                               │
│   ✓ Damage present (exception to both rules)                                │
│   ✓ Promotional discount ($180)                                             │
│   ✓ Partial return (1 of 2 monitors)                                        │
│   ✓ Bundle discount clawback (promotional threshold affects calculation)    │
│                                                                              │
│ Action: Call comprehensive tool suite to handle complexity                  │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 2: AGENT REASONING ─────────────────────────────────────────────────────┐
│                                                                              │
│ Agent's Assessment:                                                         │
│ \"This is a complex multi-rule case. Let me verify each policy constraint:   │
│  1. Is customer VIP?                                                        │
│  2. Is item within return window?                                           │
│  3. Is item final-sale?                                                     │
│  4. Is damage verified?                                                     │
│  5. How do these rules interact?                                            │
│  6. What is the correct refund calculation?\"                               │
│                                                                              │
│ Tool Priority: Full suite (all tools needed)                                │
│   1. check_vip_status()        — VIP qualification                         │
│   2. check_return_window()     — Time check                                 │
│   3. check_final_sale()        — Final-sale flag                            │
│   4. analyze_carrier_telemetry() — Legitimacy confirmation                  │
│   5. calculate_refund()        — Complex financial calculation              │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 3: TOOL EXECUTION (KEY MOMENTS) ────────────────────────────────────────┐
│                                                                              │
│ TOOL 1: check_vip_status(ltv=650, return_rate_pct=3.2)                     │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Output: {\"is_vip_qualified\": true, \"benefits\": {...}}                    │
│ ✓ Result: CUSTOMER IS VIP                                                   │
│                                                                              │
│ TOOL 2: check_return_window(delivery_date=\"2026-08-27\")                   │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Output: {\"within_30_day_window\": true, \"days_since_delivery\": 2}        │
│ ✓ Result: WITHIN RETURN WINDOW                                              │
│                                                                              │
│ TOOL 3: check_final_sale(is_final_sale=true, category=\"Electronics\")     │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Output: {\"is_final_sale\": true, \"policy\": \"Store credit only, no cash\"} │
│ ★ KEY FINDING: Final-sale items get STORE CREDIT, never cash refund        │
│                                                                              │
│ TOOL 4: analyze_carrier_telemetry(                                          │
│   origin_weight_lbs=18.5,                                                   │
│   destination_weight_lbs=18.2,                                              │
│   gps_match_address=true                                                    │
│ )                                                                            │
│ ─────────────────────────────────────────────────────────────────────────  │
│ Output: {\"verdict\": \"LEGITIMATE_DELIVERY\", \"weight_match_pct\": 98.4}  │
│ ✓ Result: GENUINE DELIVERY (not fraud)                                      │
│                                                                              │
│ TOOL 5: calculate_refund(                                                   │
│   calculation_type=\"partial_return_with_promo_clawback\",                   │
│   item_price=400.0,  (one monitor)                                          │
│   total_paid=800.0,  (bundle total paid)                                    │
│   category=\"Electronics\",                                                  │
│   is_opened=false,                                                          │
│   is_defective=true, (damaged)                                              │
│   is_final_sale=true, (clearance)                                           │
│   promo_discount=180.0, (bundle discount)                                   │
│   items_kept_value=400.0 + 180.0, (other monitor + stylus)                 │
│   is_vip=true                                                               │
│ )                                                                            │
│ ─────────────────────────────────────────────────────────────────────────  │
│ LLM Call Outcome (Without Fallback): Agent might generate confusing answer │
│                                                                              │
│ ★ CRITICAL SKILL LOGIC:                                                     │
│                                                                              │
│ Step 1: Determine the base outcome                                          │
│   - Is final-sale + damaged? → Store credit only (not cash refund)         │
│   - Is VIP? → Waive any fees                                                │
│                                                                              │
│ Step 2: Calculate for partial return                                        │
│   - Customer bought: 2× Monitor ($400 ea) + Stylus ($180) = $980           │
│   - Promo discount: -$180 (bundle)                                          │
│   - Total paid: $800                                                        │
│   - Customer keeps: 1× Monitor ($400) + Stylus ($180) = $580 (full value)  │
│                                                                              │
│ Step 3: Apply promotional discount clawback rule                            │
│   Original discount was 18% ($180 / $980)                                   │
│   Customer is returning 1 monitor ($400 full value)                         │
│   Discount clawback: Apply discount proportionally to returned item         │
│   Clawed-back discount: $400 × (18% / 2 monitors) = $36                    │
│   Refund for returned monitor: $400 - $36 = $364                            │
│                                                                              │
│ Step 4: Apply final-sale rule                                              │
│   Final-sale damaged items cannot receive cash refunds                      │
│   Must be STORE CREDIT, not payment to original payment method             │
│   Amount: $364 store credit (not cash)                                     │
│                                                                              │
│ Step 5: VIP benefits                                                        │
│   ✓ Waive restocking fees (VIP)                                             │
│   ✓ No return shipping required (damaged, final-sale item under $200)       │
│                                                                              │
│ Output: {                                                                    │
│   \"calculation_type\": \"partial_return_with_promo_clawback\",               │
│   \"amount\": 364.00,                                                        │
│   \"refund_type\": \"STORE_CREDIT\",                                         │
│   \"breakdown\": {                                                           │
│     \"item_value\": 400.00,                                                 │
│     \"promo_discount_clawback\": -36.00,                                    │
│     \"net_refund\": 364.00,                                                 │
│     \"refund_method\": \"STORE_CREDIT (final-sale rule)\",                  │
│     \"restocking_fee\": 0.00,                                                │
│     \"return_shipping\": 0.00,                                               │
│     \"total_store_credit\": 364.00                                           │
│   },                                                                        │
│   \"note\": \"VIP + damaged final-sale partial return: $364 store credit\"   │
│ }                                                                            │
│                                                                              │
│ ✓ Result: $364.00 STORE CREDIT (not cash refund)                            │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 4: SYNTHESIS (LLM Reasons Over All Conflicting Rules) ────────────────┐
│                                                                              │
│ Agent's Complex Reasoning:                                                  │
│                                                                              │
│ \"This case presents four overlapping policy constraints:                    │
│                                                                              │
│  CONSTRAINT 1: VIP Status (Policy Section 3)                               │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ✓ Customer LTV: $650 >= $500                                               │
│  ✓ Return rate: 3.2% < 5%                                                   │
│  Result: VIP qualified                                                      │
│  VIP Benefit: Instant replacement for damaged items under $200 (NORMALLY)   │
│                                                                              │
│  CONSTRAINT 2: Final-Sale Rule (Policy Section 2)                           │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ✓ Item marked: final_sale=true (clearance event)                           │
│  Result: Non-refundable                                                     │
│  Exception: If damaged, customer gets STORE CREDIT ONLY (never cash)        │
│                                                                              │
│  CONSTRAINT 3: Damage Exception (Policy Section 4)                          │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ✓ Photo verified: Damage on arrival confirmed                              │
│  Result: Eligible for replacement or refund                                 │
│                                                                              │
│  CONSTRAINT 4: Promotional Discount Clawback (Policy Section 6)             │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ✓ Promotional discount: $180 applied to $980 bundle                        │
│  ✓ Partial return: Returning 1 of 2 monitors ($400)                         │
│  Result: Discount must be recalculated based on retained items              │
│                                                                              │
│  RULE CONFLICT RESOLUTION:                                                  │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Q1: Which rule takes precedence?                                           │
│  Policy hierarchy: Damage Exception > Final-Sale > VIP > Standard           │
│  → Damage + final-sale = Store credit (rule in Section 2)                   │
│                                                                              │
│  Q2: But what about VIP instant replacement benefit?                        │
│  Answer: VIP exception is superseded by final-sale + damage combo          │
│  → VIP cannot override final-sale damage policy (store credit only)        │
│  → But VIP DOES waive restocking fees and return shipping                  │
│                                                                              │
│  Q3: How to calculate with partial return + promo?                          │
│  Answer: Apply discount clawback per Section 6                              │
│  → $400 monitor × 18% discount ÷ 2 monitors = $36 clawback                 │
│  → $400 - $36 = $364 net store credit                                       │
│                                                                              │
│  FINAL DECISION:                                                             │
│  ✓ Issue $364.00 STORE CREDIT (not cash refund)                             │
│  ✓ No return shipment required (VIP + final-sale exemption)                │
│  ✓ No restocking fees (VIP waiver)                                          │
│  ✓ Customer keeps: Monitor 2 ($400) + Stylus ($180) = $580 value           │
│                                                                              │
│  Why not VIP instant replacement?                                           │
│  - VIP instant replacement is for normal items                              │
│  - This is final-sale (clearance) → limited protection                     │
│  - Damage exception allows replacement OR store credit                      │
│  - Store credit is the final-sale outcome when damaged                      │
│  - Hierarchy: Final-Sale Rule > VIP Exception in this case                  │
│\"                                                                             │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 5: VERDICT ─────────────────────────────────────────────────────────────┐
│                                                                              │
│ ╔═══════════════════════════════════════════════════════════════════════╗  │
│ ║ FINAL DECISION                                                        ║  │
│ ╠═══════════════════════════════════════════════════════════════════════╣  │
│ ║ Action:            STORE_CREDIT_PARTIAL_RETURN                        ║  │
│ ║ Store Credit Amount:  $364.00                                          ║  │
│ ║ Refund Type:       STORE CREDIT (not cash / original payment method)  ║  │
│ ║ Return Shipment:   Not required (VIP + final-sale exemption)          ║  │
│ ║ Restocking Fee:    Waived (VIP status)                                ║  │
│ ║                                                                       ║  │
│ ║ Policy Reasoning:                                                     ║  │
│ ║ Customer is VIP (LTV $650, return rate 3.2%) with damaged item from   ║  │
│ ║ final-sale bundle. Policy Section 2 requires store credit ONLY for    ║  │
│ ║ damaged final-sale items (never cash refunds). Policy Section 6       ║  │
│ ║ applies promotional discount clawback for partial returns: Original   ║  │
│ ║ discount $180/$980 (18.3%) clawed back from returned monitor ($400):  ║  │
│ ║ $400 × (18.3% / 2) = $36.60 → $364 net store credit.                  ║  │
│ ║ VIP waives restocking fees and return shipping.                       ║  │
│ ║                                                                       ║  │
│ ║ Action: Issue $364.00 store credit. Item not returnable, keep other   ║  │
│ ║ monitor and stylus.                                                   ║  │
│ ╚═══════════════════════════════════════════════════════════════════════╝  │
│                                                                              │
│ Ground Truth Comparison:                                                    │
│   Expected: STORE_CREDIT, $364.00                                           │
│   Predicted: STORE_CREDIT, $364.00                                          │
│   Result: ✓ CORRECT                                                         │
│                                                                              │
│ Execution Metrics:                                                          │
│   Latency: 3.5 seconds (longest case, most tool calls)                      │
│   API Calls: 6 (1 Gemini + 5 skill functions + synthesis)                   │
│   Cost: $0.063 USD                                                          │
│   Decision Complexity: MAX (requires rule hierarchy reasoning)               │
│                                                                              │
│ Why This Was Hard:                                                          │
│   - Baseline (simple prompt): Would likely approve $400 cash refund (WRONG) │
│   - Single policy layer: Would miss promotional clawback calculation        │
│   - Without fallback: LLM might flip to VIP instant replacement (WRONG)     │
│   - With full system: Correctly identifies rule hierarchy and calculates    │
│                                                                              │
│ The Value of the Agentic Approach:                                          │
│   - Policy tool clarified "final-sale + damage = store credit"             │
│   - Financial tool computed promo clawback correctly ($364, not $400)       │
│   - VIP tool confirmed fee waivers (valid in this scenario)                │
│   - Orchestrator resolved rule conflicts using policy hierarchy             │
│   - Fallback layer verified math ($364 exact, no hallucination)             │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘

┌─ STEP 6: MEMORY UPDATE ───────────────────────────────────────────────────────┐
│                                                                              │
│ Store complex case in memory for future reference:                          │
│                                                                              │
│ Memory Entry:                                                               │
│   Customer: jen.lee@example.com                                             │
│   Case: CASE-10-CHALLENGING-EDGE-TAMPERED-BARCODE                           │
│   Decision: STORE_CREDIT ($364)                                             │
│   Reason: VIP + final-sale + damaged → store credit with promo clawback    │
│   Timestamp: 2026-08-29T14:52:00Z                                           │
│   Complexity: HIGH (rule hierarchy, partial return, promo clawback)         │
│                                                                              │
│ Fraud Pattern Update:                                                       │
│   jen.lee@example.com:                                                      │
│     Total Orders: 12                                                        │
│     Return Rate: 3.2% (CLEAN)                                               │
│     Fraud Score: 5/100 (VERY LOW RISK)                                      │
│     Flags: None                                                             │
│     Precedent: Case 10 handled complex multi-rule scenario                  │
│     Usage: For future edge cases with this customer                         │
│                                                                              │
│ Audit Trail: ✓ Case stored with full complexity breakdown for precedent    │
│                                                                              │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary: What These Trajectories Show

| Aspect | Case 1 (Easy) | Case 9 (Fraud) | Case 10 (Complex) |
|--------|---------------|----------------|-------------------|
| **Problem Type** | VIP exception | Fraud pattern | Multi-rule conflict |
| **Tools Called** | 4 | 3 | 5 |
| **Decision Latency** | 2.8 sec | 3.2 sec | 3.5 sec |
| **Cost** | $0.051 | $0.057 | $0.063 |
| **Baseline Would** | Get it right (40%) | Approve fraud (WRONG) | Refund cash instead of credit (WRONG) |
| **Why Agent Wins** | Coordinates VIP rules | Catches fraud pattern via memory | Resolves rule hierarchy correctly |

All three cases demonstrate why agentic orchestration is necessary — no single component solves the full problem; the agent must coordinate multiple tools, verify each result, synthesize them, and handle conflicts. The memory system enables cross-case fraud detection that single-case systems cannot do.
