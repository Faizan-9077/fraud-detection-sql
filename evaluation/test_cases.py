TEST_CASES = [
    {
        "question": "Show all transactions above ₹5 lakh.",
        "expected_view": "vw_transaction_core",
        "expected_keywords": [
            "amount > 500000"
        ]
    },
    {
        "question": "Show failed transactions.",
        "expected_view": "vw_transaction_core",
        "expected_keywords": [
            "txn_status",
            "FAILED"
        ]
    },
    {
        "question": "Show transactions between 11 PM and 4 AM.",
        "expected_view": "vw_transaction_core",
        "expected_keywords": [
            "txn_hour"
        ]
    },
    {
        "question": "Show high-risk customers.",
        "expected_view": "vw_customer_risk_profile",
        "expected_keywords": [
            "risk_rating",
            "HIGH"
        ]
    },
    {
        "question": "Show customers with open AML alerts.",
        "expected_view": "vw_customer_risk_profile",
        "expected_keywords": [
            "open_alerts"
        ]
    },
    {
        "question": "Show transactions involving FATF high-risk countries.",
        "expected_view": "vw_cross_border_risk",
        "expected_keywords": [
            "risk_level",
            "HIGH"
        ]
    },
    {
        "question": "Show transactions to FATF blacklisted countries.",
        "expected_view": "vw_cross_border_risk",
        "expected_keywords": [
            "fatf_list_type",
            "BLACKLIST"
        ]
    },
    {
        "question": "Show possible structuring activity.",
        "expected_view": "vw_structuring_detection",
        "expected_keywords": [
            "180000",
            "199999"
        ]
    },
    {
        "question": "Show possible account takeover cases.",
        "expected_view": "vw_account_takeover_signal",
        "expected_keywords": [
            "DEVICE_MISMATCH"
        ]
    },
    {
        "question": "Show impossible travel cases.",
        "expected_view": "vw_impossible_travel",
        "expected_keywords": [
            "IMPOSSIBLE_TRAVEL"
        ]
    },
    {
        "question": "Show the top 10 customers by cross-border transaction volume.",
        "expected_view": "vw_cross_border_risk",
        "expected_keywords": [
            "SUM",
            "GROUP BY"
        ]
    },
    {
        "question": "Show branches with the highest number of AML alerts.",
        "expected_view": "vw_branch_concentration_risk",
        "expected_keywords": [
            "ORDER BY"
        ]
    },
    {
        "question": "Show accounts with more than 20 transactions in one hour.",
        "expected_view": "vw_velocity_rapid_fire",
        "expected_keywords": [
            "txns_in_last_1hr"
        ]
    },
    {
        "question": "Show accounts that moved more than ₹10 lakh in one hour.",
        "expected_view": "vw_velocity_rapid_fire",
        "expected_keywords": [
            "amount_in_last_1hr"
        ]
    },
    {
        "question": "Show shared beneficiaries used by multiple customers.",
        "expected_view": "vw_shared_beneficiary_network",
        "expected_keywords": [
            "source_account_count"
        ]
    },
    {
        "question": "Show high-risk beneficiary networks.",
        "expected_view": "vw_shared_beneficiary_network",
        "expected_keywords": [
            "high_risk_senders"
        ]
    },
    {
        "question": "Show customers with expired KYC.",
        "expected_view": "vw_kyc_lapsed_high_risk",
        "expected_keywords": [
            "EXPIRED"
        ]
    },
    {
        "question": "Generate SAR evidence packets for open alerts.",
        "expected_view": "vw_sar_evidence_packet",
        "expected_keywords": [
            "OPEN"
        ]
    },
    {
        "question": "Show alerts that breached SLA.",
        "expected_view": "vw_alert_aging_sla",
        "expected_keywords": [
            "sla_status"
        ]
    }
]