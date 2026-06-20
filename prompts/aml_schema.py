# prompts/aml_schema.py

AML_SCHEMAS = {

    "cross_border": """
vw_cross_border_risk
Purpose: FATF, cross-border, international transfers
Columns:
txn_id, txn_time, amount,
customer_id, customer_name,
destination_country, risk_level,
fatf_list_type, risk_score
""",

    "structuring": """
vw_structuring_detection
Purpose: structuring, smurfing, CTR avoidance
Columns:
txn_id, txn_time, amount,
account_id, customer_id,
customer_name, ctr_id
""",

    "dormant": """
vw_dormant_account_activity
Purpose: dormant accounts, reactivation
Columns:
account_id, customer_id,
customer_name, txn_id,
txn_time, amount,
days_since_last_active
""",

    "alerts": """
vw_aml_alert_investigation
Purpose: AML alerts, investigations
Columns:
alert_id, alert_type,
severity, alert_status,
customer_id, customer_name,
txn_id, amount
""",

    "risk": """
vw_customer_risk_profile
Purpose: customer risk, compliance
Columns:
customer_id, customer_name,
risk_rating, kyc_status,
account_id, open_alerts,
total_alerts
""",

    "velocity": """
vw_velocity_rapid_fire
Purpose: velocity fraud, rapid transactions
Columns:
account_id, customer_id,
customer_name,
txns_in_last_1hr,
amount_in_last_1hr,
txns_in_last_24hr
""",

    "takeover": """
vw_account_takeover_signal
Purpose: account takeover, device mismatch
Columns:
customer_id, customer_name,
txn_id, amount,
device_match_status,
minutes_between_login_and_txn
""",

    "kyc": """
vw_kyc_lapsed_high_risk
Purpose: expired KYC, compliance risk
Columns:
customer_id, customer_name,
risk_rating, kyc_status,
kyc_overdue_days,
txns_last_30_days
""",

    "round_trip": """
vw_round_trip_detection
Purpose: round tripping, circular transfers
Columns:
txn_id, amount,
sender_account,
receiver_account_in_system,
round_trip_flag
""",

    "travel": """
vw_impossible_travel
Purpose: impossible travel, multiple countries
Columns:
customer_id,
customer_name,
login_1_country,
login_2_country,
minutes_between_logins,
travel_flag
""",

    "mule": """
vw_mule_account_pattern
Purpose: mule accounts, pass-through accounts
Columns:
account_id,
customer_id,
customer_name,
total_inflow,
total_outflow,
outflow_to_inflow_ratio
""",

    "beneficiary": """
vw_shared_beneficiary_network
Purpose: shared beneficiaries, networks
Columns:
beneficiary_account_number,
source_account_count,
unique_customers_sending,
high_risk_senders
""",

    "sla": """
vw_alert_aging_sla
Purpose: alert aging, SLA breaches
Columns:
alert_id,
severity,
alert_age_days,
sla_status,
customer_id,
customer_name
""",

    # Missing views added

    "transaction": """
vw_transaction_core
Purpose: transactions, amounts, time filters, failed transactions
Columns:
txn_id, txn_time, amount, txn_type,
channel, txn_status, account_id,
customer_id, customer_name,
risk_rating, txn_hour
""",

    "device": """
vw_device_login_anomaly
Purpose: suspicious logins, device anomalies
Columns:
login_id, login_time,
device_id, customer_id,
customer_name, login_country,
country_risk_level
""",

    "sar": """
vw_sar_evidence_packet
Purpose: SAR reports, evidence packets
Columns:
alert_id, severity,
customer_id, customer_name,
account_id, txn_id,
amount, beneficiary_country
""",

    "branch": """
vw_branch_concentration_risk
Purpose: branch AML concentration
Columns:
branch_name,
high_risk_customers,
total_alerts_30d,
high_severity_alerts
""",

    "new_account": """
vw_new_account_fraud
Purpose: new account abuse
Columns:
customer_id,
customer_name,
total_txns,
total_volume,
largest_single_txn
"""
}