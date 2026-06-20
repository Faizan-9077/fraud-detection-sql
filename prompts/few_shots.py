# prompts/few_shots.py

FEW_SHOTS = {

    "cross_border": """
Q: FATF high-risk transactions
SQL:
SELECT *
FROM vw_cross_border_risk
WHERE risk_level='HIGH'
LIMIT 100;
""",

    "structuring": """
Q: Cash transactions below CTR threshold
SQL:
SELECT *
FROM vw_structuring_detection
WHERE amount BETWEEN 180000 AND 199999
LIMIT 100;
""",

    "dormant": """
Q: Dormant accounts with recent activity
SQL:
SELECT *
FROM vw_dormant_account_activity
WHERE days_since_last_active > 90
LIMIT 100;
""",

    "alerts": """
Q: Open AML alerts
SQL:
SELECT *
FROM vw_aml_alert_investigation
WHERE alert_status='OPEN'
LIMIT 100;
""",

    "risk": """
Q: High-risk customers with open alerts
SQL:
SELECT *
FROM vw_customer_risk_profile
WHERE risk_rating='HIGH'
AND open_alerts > 0
LIMIT 100;
""",

    "velocity": """
Q: Velocity fraud activity
SQL:
SELECT *
FROM vw_velocity_rapid_fire
WHERE txns_in_last_1hr > 20
LIMIT 100;
""",

    "takeover": """
Q: Possible account takeover
SQL:
SELECT *
FROM vw_account_takeover_signal
WHERE device_match_status='DEVICE_MISMATCH'
LIMIT 100;
""",

    "kyc": """
Q: Expired KYC customers
SQL:
SELECT *
FROM vw_kyc_lapsed_high_risk
WHERE kyc_status='EXPIRED'
LIMIT 100;
""",

    "round_trip": """
Q: Round-tripping activity
SQL:
SELECT *
FROM vw_round_trip_detection
WHERE round_trip_flag='INTERNAL_LOOP'
LIMIT 100;
""",

    "travel": """
Q: Impossible travel cases
SQL:
SELECT *
FROM vw_impossible_travel
WHERE travel_flag='IMPOSSIBLE_TRAVEL'
LIMIT 100;
""",

    "mule": """
Q: Mule accounts
SQL:
SELECT *
FROM vw_mule_account_pattern
WHERE outflow_to_inflow_ratio BETWEEN 0.9 AND 1.1
LIMIT 100;
""",

    "beneficiary": """
Q: Shared beneficiaries
SQL:
SELECT *
FROM vw_shared_beneficiary_network
ORDER BY source_account_count DESC
LIMIT 100;
""",

    "sla": """
Q: SLA breaches
SQL:
SELECT *
FROM vw_alert_aging_sla
WHERE sla_status <> 'WITHIN_SLA'
LIMIT 100;
"""
}