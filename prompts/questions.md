# AML Few-Shot Hierarchy (Recommended)

## LEVEL 1 — Basic Transaction Retrieval

Question:
Show all transactions above ₹5 lakh.

SQL:
SELECT *
FROM vw_transaction_core
WHERE amount > 500000
LIMIT 100;

---

Question:
Show failed transactions.

SQL:
SELECT *
FROM vw_transaction_core
WHERE txn_status = 'FAILED'
LIMIT 100;

---

Question:
Show transactions between 11 PM and 4 AM.

SQL:
SELECT *
FROM vw_transaction_core
WHERE txn_hour >= 23
OR txn_hour <= 4
LIMIT 100;

==================================================

## LEVEL 2 — Customer & Risk Filtering

Question:
Show high-risk customers.

SQL:
SELECT *
FROM vw_customer_risk_profile
WHERE risk_rating = 'HIGH'
LIMIT 100;

---

Question:
Show customers with open AML alerts.

SQL:
SELECT *
FROM vw_customer_risk_profile
WHERE open_alerts > 0
LIMIT 100;

==================================================

## LEVEL 3 — Cross-Border Risk

Question:
Show transactions involving FATF high-risk countries.

SQL:
SELECT *
FROM vw_cross_border_risk
WHERE risk_level = 'HIGH'
LIMIT 100;

---

Question:
Show transactions to FATF blacklisted countries.

SQL:
SELECT *
FROM vw_cross_border_risk
WHERE fatf_list_type = 'BLACKLIST'
LIMIT 100;

==================================================

## LEVEL 4 — AML Detection Patterns

Question:
Show possible structuring activity.

SQL:
SELECT *
FROM vw_structuring_detection
WHERE amount BETWEEN 180000 AND 199999
LIMIT 100;

---

Question:
Show possible account takeover cases.

SQL:
SELECT *
FROM vw_account_takeover_signal
WHERE device_match_status = 'DEVICE_MISMATCH'
LIMIT 100;

---

Question:
Show impossible travel cases.

SQL:
SELECT *
FROM vw_impossible_travel
WHERE travel_flag = 'IMPOSSIBLE_TRAVEL'
LIMIT 100;

==================================================

## LEVEL 5 — Aggregation & Ranking

Question:
Show the top 10 customers by cross-border transaction volume.

SQL:
SELECT
customer_id,
customer_name,
SUM(amount) AS total_volume
FROM vw_cross_border_risk
GROUP BY customer_id, customer_name
ORDER BY total_volume DESC
LIMIT 10;

---

Question:
Show branches with the highest number of AML alerts.

SQL:
SELECT
branch_name,
total_alerts_30d
FROM vw_branch_concentration_risk
ORDER BY total_alerts_30d DESC
LIMIT 10;

==================================================

## LEVEL 6 — Velocity & Behavioral Analysis

Question:
Show accounts with more than 20 transactions in one hour.

SQL:
SELECT *
FROM vw_velocity_rapid_fire
WHERE txns_in_last_1hr > 20
LIMIT 100;

---

Question:
Show accounts that moved more than ₹10 lakh in one hour.

SQL:
SELECT *
FROM vw_velocity_rapid_fire
WHERE amount_in_last_1hr > 1000000
LIMIT 100;

==================================================

## LEVEL 7 — Network Analysis

Question:
Show shared beneficiaries used by multiple customers.

SQL:
SELECT *
FROM vw_shared_beneficiary_network
ORDER BY source_account_count DESC
LIMIT 100;

---

Question:
Show high-risk beneficiary networks.

SQL:
SELECT *
FROM vw_shared_beneficiary_network
WHERE high_risk_senders > 0
ORDER BY high_risk_senders DESC
LIMIT 100;

==================================================

## LEVEL 8 — Compliance & Investigation

Question:
Show customers with expired KYC.

SQL:
SELECT *
FROM vw_kyc_lapsed_high_risk
WHERE kyc_status = 'EXPIRED'
LIMIT 100;

---

Question:
Generate SAR evidence packets for open alerts.

SQL:
SELECT *
FROM vw_sar_evidence_packet
WHERE alert_status = 'OPEN'
LIMIT 100;

---

Question:
Show alerts that breached SLA.

SQL:
SELECT *
FROM vw_alert_aging_sla
WHERE sla_status <> 'WITHIN_SLA'
LIMIT 100;
