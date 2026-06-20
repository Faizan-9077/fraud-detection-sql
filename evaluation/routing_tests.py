ROUTING_TESTS = [

    # Transaction Core
    {
        "question": "show high value transactions",
        "expected_view": "vw_transaction_core"
    },
    {
        "question": "show transactions above 5 lakh",
        "expected_view": "vw_transaction_core"
    },
    {
        "question": "show suspicious night transactions",
        "expected_view": "vw_transaction_core"
    },
    {
        "question": "show transactions between 11pm and 4am",
        "expected_view": "vw_transaction_core"
    },

    # Cross Border
    {
        "question": "show foreign transactions",
        "expected_view": "vw_cross_border_risk"
    },
    {
        "question": "show FATF country transfers",
        "expected_view": "vw_cross_border_risk"
    },
    {
        "question": "show offshore payments",
        "expected_view": "vw_cross_border_risk"
    },
    {
        "question": "show transfers to high risk countries",
        "expected_view": "vw_cross_border_risk"
    },

    # Structuring
    {
        "question": "show structuring activity",
        "expected_view": "vw_structuring_detection"
    },
    {
        "question": "show smurfing patterns",
        "expected_view": "vw_structuring_detection"
    },
    {
        "question": "show deposits below 2 lakh",
        "expected_view": "vw_structuring_detection"
    },

    # Dormant Accounts
    {
        "question": "show dormant accounts",
        "expected_view": "vw_dormant_account_activity"
    },
    {
        "question": "show reactivated accounts",
        "expected_view": "vw_dormant_account_activity"
    },
    {
        "question": "show activity after dormancy",
        "expected_view": "vw_dormant_account_activity"
    },

    # AML Investigation
    {
        "question": "investigate suspicious activity",
        "expected_view": "vw_aml_alert_investigation"
    },
    {
        "question": "show open investigations",
        "expected_view": "vw_aml_alert_investigation"
    },
    {
        "question": "show flagged customers",
        "expected_view": "vw_aml_alert_investigation"
    },

    # Customer Risk
    {
        "question": "show high risk customers",
        "expected_view": "vw_customer_risk_profile"
    },
    {
        "question": "show customer risk profile",
        "expected_view": "vw_customer_risk_profile"
    },

    # Login Anomalies
    {
        "question": "show suspicious logins",
        "expected_view": "vw_device_login_anomaly"
    },
    {
        "question": "show foreign logins",
        "expected_view": "vw_device_login_anomaly"
    },

    # SAR
    {
        "question": "prepare sar",
        "expected_view": "vw_sar_evidence_packet"
    },
    {
        "question": "generate sar filing",
        "expected_view": "vw_sar_evidence_packet"
    },

    # Beneficiary Networks
    {
        "question": "show shared beneficiaries",
        "expected_view": "vw_shared_beneficiary_network"
    },
    {
        "question": "show linked beneficiaries",
        "expected_view": "vw_shared_beneficiary_network"
    },

    # Impossible Travel
    {
        "question": "show impossible travel",
        "expected_view": "vw_impossible_travel"
    },

    # Account Takeover
    {
        "question": "show account takeover activity",
        "expected_view": "vw_account_takeover_signal"
    },

    # KYC
    {
        "question": "show expired kyc customers",
        "expected_view": "vw_kyc_lapsed_high_risk"
    },

    # SLA
    {
        "question": "show breached alerts",
        "expected_view": "vw_alert_aging_sla"
    }
]