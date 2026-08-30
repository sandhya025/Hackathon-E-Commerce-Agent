import json
import os

cases_dir = os.path.join(os.path.dirname(__file__), "cases")
os.makedirs(cases_dir, exist_ok=True)

test_cases = [
    {
        "case_id": "CASE-01-VIP-DAMAGED",
        "title": "VIP Customer Received Damaged Smart Watch",
        "customer": {
            "name": "Sarah Jenkins",
            "email": "sarah.j@example.com",
            "ltv": 1450.00,
            "orders_count": 8,
            "historical_return_rate_pct": 2.1,
            "tier": "VIP"
        },
        "order": {
            "order_id": "ORD-1001",
            "order_date": "2026-08-15",
            "delivery_date": "2026-08-18",
            "items": [
                {"sku": "WATCH-PRO-01", "name": "Apex Pro Smartwatch", "category": "Electronics", "unit_price": 180.00, "qty": 1, "final_sale": False}
            ],
            "subtotal": 180.00,
            "discount_applied": 0.00,
            "shipping_fee": 0.00,
            "total_paid": 180.00
        },
        "carrier_telemetry": {
            "carrier": "FedEx",
            "tracking_number": "FX-88912301",
            "status": "Delivered",
            "delivery_timestamp": "2026-08-18T14:22:00Z",
            "origin_scan_weight_lbs": 1.25,
            "destination_scale_weight_lbs": 1.23,
            "gps_match_address": True,
            "carrier_exception_notes": "Delivered to recipient front door"
        },
        "ticket": {
            "subject": "Screen cracked on arrival!",
            "message": "Hi, I just opened the smartwatch package and the front display glass is completely shattered. I need a replacement as soon as possible for my marathon this weekend. Photo attached.",
            "photo_evidence_provided": True,
            "photo_verified_defect": True
        },
        "ground_truth_verdict": {
            "action": "INSTANT_FREE_REPLACEMENT",
            "refund_amount": 0.00,
            "return_shipment_required": False,
            "restocking_fee": 0.00,
            "policy_reasoning": "Customer is VIP (LTV $1450 >= $500, Return rate 2.1% < 5%). Damaged item under $200 qualifies for immediate 1-click replacement without requiring return shipment."
        }
    },
    {
        "case_id": "CASE-02-EMPTY-BOX-FRAUD",
        "title": "Empty Box Claim with Critical Weight Delta",
        "customer": {
            "name": "Marcus Vance",
            "email": "m.vance88@example.com",
            "ltv": 920.00,
            "orders_count": 3,
            "historical_return_rate_pct": 66.7,
            "tier": "Standard"
        },
        "order": {
            "order_id": "ORD-1002",
            "order_date": "2026-08-10",
            "delivery_date": "2026-08-14",
            "items": [
                {"sku": "AUDIO-NOISE-MAX", "name": "Studio Master Headphones", "category": "Electronics", "unit_price": 420.00, "qty": 1, "final_sale": False}
            ],
            "subtotal": 420.00,
            "discount_applied": 0.00,
            "shipping_fee": 0.00,
            "total_paid": 420.00
        },
        "carrier_telemetry": {
            "carrier": "UPS",
            "tracking_number": "1Z999AA10123456784",
            "status": "Delivered",
            "delivery_timestamp": "2026-08-14T11:05:00Z",
            "origin_scan_weight_lbs": 3.80,
            "destination_scale_weight_lbs": 3.78,
            "gps_match_address": True,
            "carrier_exception_notes": "Delivered to porch with proof photo"
        },
        "ticket": {
            "subject": "The box was EMPTY! Scam!",
            "message": "I opened the box and there were only packing peanuts inside, no headphones! Refund my $420 immediately or I will contact my bank to initiate a chargeback.",
            "photo_evidence_provided": True,
            "photo_verified_defect": False
        },
        "ground_truth_verdict": {
            "action": "REJECT_REFUND_ESCALATE_FRAUD",
            "refund_amount": 0.00,
            "return_shipment_required": False,
            "restocking_fee": 0.00,
            "policy_reasoning": "UPS destination scale weight at local delivery hub was 3.78 lbs, matching origin weight of 3.80 lbs. Package could not have been delivered empty. High historical return rate (66.7%). Deny instant refund and escalate to fraud investigation."
        }
    },
    {
        "case_id": "CASE-03-SPLIT-BUNDLE-DISCOUNT",
        "title": "Partial Return of Buy-2-Get-1-Free Bundle",
        "customer": {
            "name": "Emily Watson",
            "email": "emily.w@example.com",
            "ltv": 320.00,
            "orders_count": 2,
            "historical_return_rate_pct": 0.0,
            "tier": "Standard"
        },
        "order": {
            "order_id": "ORD-1003",
            "order_date": "2026-08-01",
            "delivery_date": "2026-08-05",
            "items": [
                {"sku": "SHIRT-LINEN-01", "name": "Classic Linen Shirt", "category": "Apparel", "unit_price": 50.00, "qty": 1, "final_sale": False},
                {"sku": "SHIRT-LINEN-02", "name": "Classic Linen Shirt (Blue)", "category": "Apparel", "unit_price": 50.00, "qty": 1, "final_sale": False},
                {"sku": "SHIRT-LINEN-03", "name": "Classic Linen Shirt (Olive)", "category": "Apparel", "unit_price": 50.00, "qty": 1, "final_sale": False}
            ],
            "subtotal": 150.00,
            "discount_applied": 50.00,
            "shipping_fee": 0.00,
            "total_paid": 100.00
        },
        "carrier_telemetry": {
            "carrier": "USPS",
            "tracking_number": "9400111899223344556677",
            "status": "Delivered",
            "delivery_timestamp": "2026-08-05T16:45:00Z",
            "origin_scan_weight_lbs": 1.90,
            "destination_scale_weight_lbs": 1.90,
            "gps_match_address": True,
            "carrier_exception_notes": "Delivered in mailbox"
        },
        "ticket": {
            "subject": "Want to return the Olive Linen Shirt",
            "message": "I love the first two shirts, but the Olive one doesn't suit my complexion. I want to return the Olive shirt for a $50 refund please.",
            "photo_evidence_provided": False,
            "photo_verified_defect": False
        },
        "ground_truth_verdict": {
            "action": "APPROVE_PARTIAL_REFUND_WITH_RMA",
            "refund_amount": 0.00,
            "return_shipment_required": True,
            "restocking_fee": 0.00,
            "policy_reasoning": "Customer bought 3 shirts under Buy-2-Get-1-Free promo for $100 ($50 off). Returning 1 shirt leaves 2 shirts ($100 standard price). Recalculated total owed is $100, meaning refund amount is $0.00 if returning the free item, or store credit adjusted. Apparel return shipping is free."
        }
    },
    {
        "case_id": "CASE-04-FINAL-SALE-DAMAGED",
        "title": "Damaged Final Sale Clearance Item",
        "customer": {
            "name": "David Chen",
            "email": "dchen@example.com",
            "ltv": 210.00,
            "orders_count": 1,
            "historical_return_rate_pct": 0.0,
            "tier": "Standard"
        },
        "order": {
            "order_id": "ORD-1004",
            "order_date": "2026-08-12",
            "delivery_date": "2026-08-16",
            "items": [
                {"sku": "CERAMIC-VASE-CLR", "name": "Artisan Ceramic Vase", "category": "Home", "unit_price": 75.00, "qty": 1, "final_sale": True}
            ],
            "subtotal": 75.00,
            "discount_applied": 37.50,
            "shipping_fee": 5.99,
            "total_paid": 43.49
        },
        "carrier_telemetry": {
            "carrier": "FedEx",
            "tracking_number": "FX-90023411",
            "status": "Delivered",
            "delivery_timestamp": "2026-08-16T10:12:00Z",
            "origin_scan_weight_lbs": 4.10,
            "destination_scale_weight_lbs": 4.05,
            "gps_match_address": True,
            "carrier_exception_notes": "Delivered to door"
        },
        "ticket": {
            "subject": "Clearance vase arrived in pieces",
            "message": "I know this was a clearance sale item, but it arrived smashed into shards. I want a refund back to my Visa card.",
            "photo_evidence_provided": True,
            "photo_verified_defect": True
        },
        "ground_truth_verdict": {
            "action": "APPROVE_STORE_CREDIT_ONLY",
            "refund_amount": 43.49,
            "return_shipment_required": False,
            "restocking_fee": 0.00,
            "policy_reasoning": "Item is marked final_sale: True. Per Section 2 of Store Policy, damaged final-sale items receive Store Credit Only ($43.49), never cash refund to original payment method. No return shipment required for broken ceramic."
        }
    },
    {
        "case_id": "CASE-05-CARRIER-MISDELIVERY",
        "title": "Delivered Status but GPS Location Mismatch",
        "customer": {
            "name": "Rachel Adams",
            "email": "radams.design@example.com",
            "ltv": 450.00,
            "orders_count": 4,
            "historical_return_rate_pct": 0.0,
            "tier": "Standard"
        },
        "order": {
            "order_id": "ORD-1005",
            "order_date": "2026-08-18",
            "delivery_date": "2026-08-22",
            "items": [
                {"sku": "DESK-LAMP-LED", "name": "Architect LED Desk Lamp", "category": "Home", "unit_price": 89.00, "qty": 1, "final_sale": False}
            ],
            "subtotal": 89.00,
            "discount_applied": 0.00,
            "shipping_fee": 0.00,
            "total_paid": 89.00
        },
        "carrier_telemetry": {
            "carrier": "UPS",
            "tracking_number": "1Z555AA99887766554",
            "status": "Delivered",
            "delivery_timestamp": "2026-08-22T15:30:00Z",
            "origin_scan_weight_lbs": 3.20,
            "destination_scale_weight_lbs": 3.20,
            "gps_match_address": False,
            "carrier_exception_notes": "GPS scan shows driver delivered 2.4 miles away at wrong street address"
        },
        "ticket": {
            "subject": "Tracking says delivered but nothing is here",
            "message": "UPS tracking shows delivered at 3:30 PM today, but I was home and nothing was dropped off. I checked with my neighbors too.",
            "photo_evidence_provided": False,
            "photo_verified_defect": False
        },
        "ground_truth_verdict": {
            "action": "INSTANT_FREE_REPLACEMENT",
            "refund_amount": 0.00,
            "return_shipment_required": False,
            "restocking_fee": 0.00,
            "policy_reasoning": "Carrier telemetry confirms gps_match_address: False (misdelivered 2.4 miles away). Per Section 5, issue instant replacement and file back-office carrier misdelivery claim."
        }
    },
    {
        "case_id": "CASE-06-OPENED-ELECTRONIC-RETURN",
        "title": "Opened Non-Defective Electronics Return",
        "customer": {
            "name": "Brian Miller",
            "email": "brian.miller9@example.com",
            "ltv": 150.00,
            "orders_count": 1,
            "historical_return_rate_pct": 0.0,
            "tier": "Standard"
        },
        "order": {
            "order_id": "ORD-1006",
            "order_date": "2026-08-14",
            "delivery_date": "2026-08-17",
            "items": [
                {"sku": "KEYBOARD-MECH-RGB", "name": "Pro Wireless Mechanical Keyboard", "category": "Electronics", "unit_price": 120.00, "qty": 1, "final_sale": False}
            ],
            "subtotal": 120.00,
            "discount_applied": 0.00,
            "shipping_fee": 5.99,
            "total_paid": 125.99
        },
        "carrier_telemetry": {
            "carrier": "FedEx",
            "tracking_number": "FX-44910293",
            "status": "Delivered",
            "delivery_timestamp": "2026-08-17T12:00:00Z",
            "origin_scan_weight_lbs": 2.80,
            "destination_scale_weight_lbs": 2.80,
            "gps_match_address": True,
            "carrier_exception_notes": "Delivered"
        },
        "ticket": {
            "subject": "Want to return keyboard - don't like key switches",
            "message": "I unboxed the keyboard and used it for 2 days. It works fine, but the switches are too clicky for my office. I want to return it for a refund.",
            "photo_evidence_provided": False,
            "photo_verified_defect": False
        },
        "ground_truth_verdict": {
            "action": "APPROVE_RETURN_WITH_FEES",
            "refund_amount": 99.01,
            "return_shipment_required": True,
            "restocking_fee": 15.00,
            "return_shipping_deduction": 5.99,
            "policy_reasoning": "Opened non-defective electronics item is subject to $15.00 restocking fee and $5.99 return shipping deduction. Net refund on $120 item = $120 - $15 - $5.99 = $99.01 (original shipping fee not refunded)."
        }
    },
    {
        "case_id": "CASE-07-EXPIRED-RETURN-WINDOW",
        "title": "Return Request Past 30-Day Window",
        "customer": {
            "name": "Jessica Taylor",
            "email": "jtaylor@example.com",
            "ltv": 280.00,
            "orders_count": 2,
            "historical_return_rate_pct": 0.0,
            "tier": "Standard"
        },
        "order": {
            "order_id": "ORD-1007",
            "order_date": "2026-06-10",
            "delivery_date": "2026-06-15",
            "items": [
                {"sku": "SHOES-RUN-PRO", "name": "Aero Sprint Running Shoes", "category": "Shoes", "unit_price": 140.00, "qty": 1, "final_sale": False}
            ],
            "subtotal": 140.00,
            "discount_applied": 0.00,
            "shipping_fee": 0.00,
            "total_paid": 140.00
        },
        "carrier_telemetry": {
            "carrier": "USPS",
            "tracking_number": "9405511299887766112233",
            "status": "Delivered",
            "delivery_timestamp": "2026-06-15T11:20:00Z",
            "origin_scan_weight_lbs": 2.10,
            "destination_scale_weight_lbs": 2.10,
            "gps_match_address": True,
            "carrier_exception_notes": "Delivered"
        },
        "ticket": {
            "subject": "Need to return shoes",
            "message": "Hi, I bought these shoes in June and forgot about them in my closet. They are unworn in the box. Can I get a return label and refund?",
            "photo_evidence_provided": False,
            "photo_verified_defect": False
        },
        "ground_truth_verdict": {
            "action": "REJECT_RETURN_EXPIRED_WINDOW",
            "refund_amount": 0.00,
            "return_shipment_required": False,
            "restocking_fee": 0.00,
            "policy_reasoning": "Delivered on June 15, 2026 (75 days ago). Section 1 strictly enforces a 30-day return window. Customer is not VIP. Politely decline return request."
        }
    },
    {
        "case_id": "CASE-08-DAMAGED-BOX-INTACT-ITEM",
        "title": "Damaged Outer Box with Intact Product",
        "customer": {
            "name": "Kevin Peterson",
            "email": "k.peterson@example.com",
            "ltv": 380.00,
            "orders_count": 3,
            "historical_return_rate_pct": 0.0,
            "tier": "Standard"
        },
        "order": {
            "order_id": "ORD-1008",
            "order_date": "2026-08-20",
            "delivery_date": "2026-08-24",
            "items": [
                {"sku": "ESPRESSO-POT-SS", "name": "Stainless Steel Espresso Maker", "category": "Home", "unit_price": 60.00, "qty": 1, "final_sale": False}
            ],
            "subtotal": 60.00,
            "discount_applied": 0.00,
            "shipping_fee": 0.00,
            "total_paid": 60.00
        },
        "carrier_telemetry": {
            "carrier": "FedEx",
            "tracking_number": "FX-77610022",
            "status": "Delivered",
            "delivery_timestamp": "2026-08-24T16:10:00Z",
            "origin_scan_weight_lbs": 3.00,
            "destination_scale_weight_lbs": 3.00,
            "gps_match_address": True,
            "carrier_exception_notes": "Outer carton creased"
        },
        "ticket": {
            "subject": "The shipping box was beat up and torn",
            "message": "The outer packaging was severely crushed. The espresso maker itself seems fine and works, but for a new purchase the packaging looked terrible. What can you do for me?",
            "photo_evidence_provided": True,
            "photo_verified_defect": False
        },
        "ground_truth_verdict": {
            "action": "APPROVE_GOODWILL_PARTIAL_REFUND",
            "refund_amount": 9.00,
            "return_shipment_required": False,
            "restocking_fee": 0.00,
            "policy_reasoning": "Per Section 4, if packaging is damaged but the product inside is intact and functional, offer a 15% goodwill partial refund (15% of $60.00 = $9.00), with no return shipment required."
        }
    },
    {
        "case_id": "CASE-09-SERIAL-RETURNER-ABUSE",
        "title": "Serial Wardrober Abusing Free Returns",
        "customer": {
            "name": "Chloe Bennett",
            "email": "chloe.b.style@example.com",
            "ltv": 1200.00,
            "orders_count": 7,
            "historical_return_rate_pct": 71.4,
            "tier": "Standard"
        },
        "order": {
            "order_id": "ORD-1009",
            "order_date": "2026-08-16",
            "delivery_date": "2026-08-19",
            "items": [
                {"sku": "DRESS-SILK-EVENING", "name": "Silk Evening Gown", "category": "Apparel", "unit_price": 350.00, "qty": 1, "final_sale": False}
            ],
            "subtotal": 350.00,
            "discount_applied": 0.00,
            "shipping_fee": 0.00,
            "total_paid": 350.00
        },
        "carrier_telemetry": {
            "carrier": "UPS",
            "tracking_number": "1Z333BB11223344556",
            "status": "Delivered",
            "delivery_timestamp": "2026-08-19T13:40:00Z",
            "origin_scan_weight_lbs": 1.50,
            "destination_scale_weight_lbs": 1.50,
            "gps_match_address": True,
            "carrier_exception_notes": "Delivered"
        },
        "ticket": {
            "subject": "Returning the silk gown",
            "message": "Wore it to an event on Saturday, now returning it. Send me my free return label and full $350 refund immediately.",
            "photo_evidence_provided": False,
            "photo_verified_defect": False
        },
        "ground_truth_verdict": {
            "action": "ESCALATE_MANUAL_FRAUD_REVIEW",
            "refund_amount": 0.00,
            "return_shipment_required": False,
            "restocking_fee": 0.00,
            "policy_reasoning": "Customer admitted wearing the garment ('wore it to an event') and has a 71.4% return rate across 7 orders (violates wardrobing policy and Section 5 serial return abuse threshold >=50%). Escalate for manual fraud and condition inspection."
        }
    },
    {
        "case_id": "CASE-10-CHALLENGING-EDGE-TAMPERED-BARCODE",
        "title": "Challenging Edge Case: Weight Scan Intercepted in Transit",
        "customer": {
            "name": "Alexander Hayes",
            "email": "ahayes.tech@example.com",
            "ltv": 610.00,
            "orders_count": 4,
            "historical_return_rate_pct": 0.0,
            "tier": "VIP"
        },
        "order": {
            "order_id": "ORD-1010",
            "order_date": "2026-08-21",
            "delivery_date": "2026-08-25",
            "items": [
                {"sku": "DRONE-4K-PRO", "name": "AeroGlide 4K Camera Drone", "category": "Electronics", "unit_price": 550.00, "qty": 1, "final_sale": False}
            ],
            "subtotal": 550.00,
            "discount_applied": 0.00,
            "shipping_fee": 0.00,
            "total_paid": 550.00
        },
        "carrier_telemetry": {
            "carrier": "FedEx",
            "tracking_number": "FX-1122339900",
            "status": "Delivered",
            "delivery_timestamp": "2026-08-25T17:15:00Z",
            "origin_scan_weight_lbs": 6.40,
            "destination_scale_weight_lbs": 0.35,
            "gps_match_address": True,
            "carrier_exception_notes": "Package was re-taped with non-standard yellow security tape at sorting hub"
        },
        "ticket": {
            "subject": "Package opened and empty - VIP member requesting resolution",
            "message": "I received my package today but the box was cut open and re-taped with yellow tape. The drone inside is missing. Since I am a VIP member, please issue my refund.",
            "photo_evidence_provided": True,
            "photo_verified_defect": True
        },
        "ground_truth_verdict": {
            "action": "ESCALATE_CARRIER_THEFT_INVESTIGATION",
            "refund_amount": 0.00,
            "return_shipment_required": False,
            "restocking_fee": 0.00,
            "policy_reasoning": "Even though customer is VIP, the claim is $550 (> $200 VIP instant replacement ceiling) AND carrier telemetry confirms major weight drop (6.40 lbs -> 0.35 lbs) with internal hub re-taping note. This is a severe internal carrier transit theft. Escalate to Priority Carrier Claims team to coordinate insurance payout and replacement approval."
        }
    }
]

for case in test_cases:
    case_path = os.path.join(cases_dir, f"{case['case_id'].lower()}.json")
    with open(case_path, "w", encoding="utf-8") as f:
        json.dump(case, f, indent=2)

print(f"Successfully generated {len(test_cases)} benchmark test cases in {cases_dir}")
