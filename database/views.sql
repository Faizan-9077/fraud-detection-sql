
--Intent: Basic transaction lookups, time-window queries, night transactions
--Covers: "Show transactions above ₹5L between 11pm–4am"



CREATE VIEW vw_transaction_core AS
SELECT
    t.txn_id,
    t.txn_time,
    t.txn_type,
    t.amount,
    t.channel,
    t.status              AS txn_status,
    t.balance_after_txn,
    a.account_id,
    a.account_type,
    a.status              AS account_status,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    EXTRACT(HOUR FROM t.txn_time) AS txn_hour
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id;


--Intent: FATF country transactions, international beneficiary transfers
--Covers: Transactions going to/from high-risk countries


CREATE VIEW vw_cross_border_risk AS
SELECT
    t.txn_id,
    t.txn_time,
    t.amount,
    t.txn_type,
    t.channel,
    a.account_id,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    b.beneficiary_name,
    b.beneficiary_account_number,
    fc.country_name       AS destination_country,
    fc.risk_level,
    fc.fatf_list_type,
    fc.risk_score,
    fc.monitoring_status
FROM transactions t
JOIN accounts a       ON t.account_id = a.account_id
JOIN customers c      ON a.customer_id = c.customer_id
JOIN beneficiaries b  ON t.beneficiary_id = b.beneficiary_id
JOIN fatf_high_risk_countries fc ON b.country_id = fc.country_id;


--Intent: Smurfing / cash deposits just below ₹2L threshold in time windows
--Covers: "Accounts with 5+ cash deposits just below ₹2L in 72 hours"

CREATE VIEW vw_structuring_detection AS
SELECT
    t.txn_id,
    t.txn_time,
    t.amount,
    t.txn_type,
    t.channel,
    a.account_id,
    a.account_type,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    c.pan_number,
    -- CTR linkage
    cl.ctr_id,
    cl.amount             AS ctr_reported_amount
FROM transactions t
JOIN accounts a  ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
LEFT JOIN ctr_log cl ON t.txn_id = cl.txn_id
WHERE t.txn_type IN ('CASH_DEPOSIT', 'CASH_WITHDRAWAL');


--Intent: Reactivated dormant accounts with sudden large transfers
--Covers: "Customers who reactivated dormant account and made large transfer within 48 hours"

CREATE VIEW vw_dormant_account_activity AS
SELECT
    a.account_id,
    a.account_type,
    a.status              AS account_status,
    a.last_active_date,
    a.balance,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    c.phone_number,
    t.txn_id,
    t.txn_time,
    t.amount,
    t.txn_type,
    t.channel,
    -- Days inactive before this transaction
    (t.txn_time::date - a.last_active_date) 
        AS days_since_last_active
FROM accounts a
JOIN customers c     ON a.customer_id = c.customer_id
JOIN transactions t  ON a.account_id = t.account_id
WHERE a.last_active_date < CURRENT_DATE - INTERVAL '90 days';

--Intent: AML alert triage, open case investigation
--Covers: Alert + linked transaction + customer full picture


CREATE VIEW vw_aml_alert_investigation AS
SELECT
    al.alert_id,
    al.alert_type,
    al.severity,
    al.status             AS alert_status,
    al.created_at         AS alert_raised_at,
    t.txn_id,
    t.txn_time,
    t.amount,
    t.txn_type,
    t.channel,
    t.status              AS txn_status,
    a.account_id,
    a.account_type,
    a.balance,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    c.pan_number,
    c.aadhar,
    k.status              AS kyc_status,
    k.review_date         AS last_kyc_date
FROM aml_alerts al
JOIN accounts a      ON al.account_id = a.account_id
JOIN customers c     ON a.customer_id = c.customer_id
LEFT JOIN transactions t  ON al.txn_id = t.txn_id
LEFT JOIN kyc_records k   ON c.customer_id = k.customer_id;

--Intent: Full risk snapshot of a customer — KYC, alerts, account health
--Covers: Risk rating queries, compliance checks


CREATE VIEW vw_customer_risk_profile AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.dob,
    c.pan_number,
    c.aadhar,
    c.phone_number,
    c.email,
    c.risk_rating,
    c.created_at          AS customer_since,
    k.kyc_id,
    k.status              AS kyc_status,
    k.review_date,
    a.account_id,
    a.account_type,
    a.balance,
    a.status              AS account_status,
    a.last_active_date,
    br.branch_name,
    br.city,
    br.state,
    -- Alert summary
    COUNT(DISTINCT al.alert_id) AS total_alerts,
    COUNT(DISTINCT CASE WHEN al.status = 'OPEN' 
          THEN al.alert_id END) AS open_alerts
FROM customers c
LEFT JOIN kyc_records k ON c.customer_id = k.customer_id
LEFT JOIN accounts a    ON c.customer_id = a.customer_id
LEFT JOIN branches br   ON a.branch_id = br.branch_id
LEFT JOIN aml_alerts al ON a.account_id = al.account_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.dob,
         c.pan_number, c.aadhar, c.phone_number, c.email,
         c.risk_rating, c.created_at, k.kyc_id, k.status,
         k.review_date, a.account_id, a.account_type,
         a.balance, a.status, a.last_active_date,
         br.branch_name, br.city, br.state;


--Intent: Suspicious login patterns — new devices, foreign IPs, multiple locations
--Covers: Device change before transaction, foreign country logins

CREATE VIEW vw_device_login_anomaly AS
SELECT
    dl.login_id,
    dl.login_time,
    dl.device_id,
    dl.ip_address,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    fc.country_name       AS login_country,
    fc.risk_level         AS country_risk_level,
    fc.fatf_list_type,
    fc.risk_score
FROM device_logins dl
JOIN customers c ON dl.customer_id = c.customer_id
LEFT JOIN fatf_high_risk_countries fc ON dl.country_id = fc.country_id;

--Intent: One-click SAR export — everything an analyst needs per case
--Covers: Full audit trail for Suspicious Activity Report filing


CREATE VIEW vw_sar_evidence_packet AS
SELECT
    al.alert_id,
    al.alert_type,
    al.severity,
    al.status             AS alert_status,
    al.created_at         AS alert_date,
    -- Customer
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.pan_number,
    c.aadhar,
    c.risk_rating,
    -- KYC
    k.status              AS kyc_status,
    k.review_date,
    -- Account
    a.account_id,
    a.account_type,
    a.balance,
    -- Branch
    br.branch_name,
    br.city,
    br.state,
    -- Transaction
    t.txn_id,
    t.txn_time,
    t.amount,
    t.txn_type,
    t.channel,
    -- Beneficiary
    b.beneficiary_name,
    b.beneficiary_account_number,
    -- Country risk
    fc.country_name       AS beneficiary_country,
    fc.risk_level,
    fc.fatf_list_type,
    -- CTR flag
    cl.ctr_id             AS ctr_filed
FROM aml_alerts al
JOIN accounts a      ON al.account_id = a.account_id
JOIN customers c     ON a.customer_id = c.customer_id
JOIN branches br     ON a.branch_id = br.branch_id
LEFT JOIN kyc_records k     ON c.customer_id = k.customer_id
LEFT JOIN transactions t    ON al.txn_id = t.txn_id
LEFT JOIN beneficiaries b   ON t.beneficiary_id = b.beneficiary_id
LEFT JOIN fatf_high_risk_countries fc ON b.country_id = fc.country_id
LEFT JOIN ctr_log cl        ON t.txn_id = cl.txn_id;


--Intent: Currency Transaction Report monitoring, near-threshold tracking
--Covers: CTR filed cases + related transaction context

CREATE VIEW vw_ctr_threshold_monitor AS
SELECT
    cl.ctr_id,
    cl.amount             AS reported_amount,
    cl.txn_time,
    a.account_id,
    a.account_type,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.pan_number,
    c.risk_rating,
    t.txn_type,
    t.channel,
    t.status              AS txn_status
FROM ctr_log cl
JOIN accounts a  ON cl.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
LEFT JOIN transactions t ON cl.txn_id = t.txn_id;


--Intent: Beneficiary reuse analysis, shared beneficiaries across accounts
--Covers: Network / round-trip fraud, mule account detection

CREATE VIEW vw_beneficiary_network_risk AS
SELECT
    b.beneficiary_id,
    b.beneficiary_name,
    b.beneficiary_account_number,
    b.created_at          AS beneficiary_added_date,
    a.account_id,
    a.account_type,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    fc.country_name       AS beneficiary_country,
    fc.risk_level,
    fc.risk_score,
    fc.fatf_list_type,
    COUNT(t.txn_id)       AS total_txns_to_beneficiary,
    SUM(t.amount)         AS total_amount_sent
FROM beneficiaries b
JOIN accounts a  ON b.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
LEFT JOIN fatf_high_risk_countries fc ON b.country_id = fc.country_id
LEFT JOIN transactions t ON b.beneficiary_id = t.beneficiary_id
GROUP BY b.beneficiary_id, b.beneficiary_name,
         b.beneficiary_account_number, b.created_at,
         a.account_id, a.account_type,
         c.customer_id, c.first_name, c.last_name,
         c.risk_rating, fc.country_name, fc.risk_level,
         fc.risk_score, fc.fatf_list_type;

--Pattern in data: Multiple rows in transactions for same account_id within a short txn_time window.

CREATE VIEW vw_velocity_rapid_fire AS
SELECT
    t.account_id,
    t.txn_id,
    t.txn_time,
    t.amount,
    t.txn_type,
    t.channel,
    t.status              AS txn_status,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    c.pan_number,
    -- Rolling window aggregates
    COUNT(t2.txn_id) OVER (
        PARTITION BY t.account_id
        ORDER BY t.txn_time
        RANGE BETWEEN INTERVAL '1 hour' PRECEDING 
              AND CURRENT ROW
    ) AS txns_in_last_1hr,
    SUM(t2.amount) OVER (
        PARTITION BY t.account_id
        ORDER BY t.txn_time
        RANGE BETWEEN INTERVAL '1 hour' PRECEDING 
              AND CURRENT ROW
    ) AS amount_in_last_1hr,
    COUNT(t3.txn_id) OVER (
        PARTITION BY t.account_id
        ORDER BY t.txn_time
        RANGE BETWEEN INTERVAL '24 hours' PRECEDING 
              AND CURRENT ROW
    ) AS txns_in_last_24hr
FROM transactions t
JOIN accounts a  ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN transactions t2 ON t2.account_id = t.account_id
JOIN transactions t3 ON t3.account_id = t.account_id;

--Pattern: device_logins.device_id doesn't match transactions.device_id, and txn_time is very close to login_time.

CREATE VIEW vw_account_takeover_signal AS
SELECT
    dl.login_id,
    dl.login_time,
    dl.device_id          AS login_device,
    dl.ip_address,
    t.txn_id,
    t.txn_time,
    t.amount,
    t.txn_type,
    t.device_id           AS txn_device,
    t.channel,
    -- Time gap between login and transaction
    EXTRACT(EPOCH FROM (t.txn_time - dl.login_time))/60 
        AS minutes_between_login_and_txn,
    -- Device mismatch flag
    CASE WHEN dl.device_id != t.device_id 
         THEN 'DEVICE_MISMATCH' 
         ELSE 'SAME_DEVICE' 
    END AS device_match_status,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    c.phone_number,
    a.account_id,
    a.balance,
    -- Login from high risk country?
    fc.country_name       AS login_country,
    fc.risk_level         AS login_country_risk
FROM device_logins dl
JOIN customers c  ON dl.customer_id = c.customer_id
JOIN accounts a   ON c.customer_id = a.customer_id
JOIN transactions t ON (
    a.account_id = t.account_id
    AND t.txn_time BETWEEN dl.login_time 
        AND dl.login_time + INTERVAL '30 minutes'
)
LEFT JOIN fatf_high_risk_countries fc 
    ON dl.country_id = fc.country_id;

--Pattern: kyc_records.review_date is old + kyc_records.status = PENDING/EXPIRED + active transactions exist.


CREATE VIEW vw_kyc_lapsed_high_risk AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    c.pan_number,
    c.phone_number,
    k.kyc_id,
    k.status              AS kyc_status,
    k.review_date,
    -- Days since KYC review
    (CURRENT_DATE - k.review_date) 
        AS kyc_overdue_days,
    a.account_id,
    a.account_type,
    a.balance,
    a.status              AS account_status,
    -- Recent transaction summary
    COUNT(t.txn_id)       AS txns_last_30_days,
    SUM(t.amount)         AS volume_last_30_days,
    MAX(t.amount)         AS largest_txn,
    MAX(t.txn_time)       AS last_txn_time,
    -- Any open alerts?
    COUNT(al.alert_id)    AS open_aml_alerts
FROM kyc_records k
JOIN customers c     ON k.customer_id = c.customer_id
JOIN accounts a      ON c.customer_id = a.customer_id
LEFT JOIN transactions t ON (
    a.account_id = t.account_id
    AND t.txn_time >= CURRENT_TIMESTAMP - INTERVAL '30 days'
)
LEFT JOIN aml_alerts al ON (
    al.account_id = a.account_id
    AND al.status = 'OPEN'
)
WHERE k.status IN ('PENDING', 'EXPIRED', 'UNDER_REVIEW')
GROUP BY c.customer_id, c.first_name, c.last_name,
         c.risk_rating, c.pan_number, c.phone_number,
         k.kyc_id, k.status, k.review_date,
         a.account_id, a.account_type, a.balance, a.status;


--Pattern: beneficiary_account_number in beneficiaries matches an account_id in accounts — the destination IS also a source account in your system.


CREATE VIEW vw_round_trip_detection AS
SELECT
    -- Sending side
    t.txn_id,
    t.txn_time,
    t.amount,
    t.txn_type,
    a_sender.account_id   AS sender_account,
    c_sender.customer_id  AS sender_customer_id,
    c_sender.first_name || ' ' || c_sender.last_name 
        AS sender_name,
    c_sender.risk_rating  AS sender_risk,
    -- Beneficiary (the destination)
    b.beneficiary_id,
    b.beneficiary_name,
    b.beneficiary_account_number,
    -- Is the beneficiary ALSO an account in our system?
    a_receiver.account_id AS receiver_account_in_system,
    c_receiver.customer_id AS receiver_customer_id,
    c_receiver.first_name || ' ' || c_receiver.last_name 
        AS receiver_name,
    c_receiver.risk_rating AS receiver_risk,
    CASE 
        WHEN a_receiver.account_id IS NOT NULL 
        THEN 'INTERNAL_LOOP' 
        ELSE 'EXTERNAL' 
    END AS round_trip_flag
FROM transactions t
JOIN accounts a_sender    ON t.account_id = a_sender.account_id
JOIN customers c_sender   ON a_sender.customer_id = c_sender.customer_id
JOIN beneficiaries b      ON t.beneficiary_id = b.beneficiary_id
-- The key join: does beneficiary account exist as one of OUR accounts?
LEFT JOIN accounts a_receiver 
    ON b.beneficiary_account_number = a_receiver.account_id
LEFT JOIN customers c_receiver 
    ON a_receiver.customer_id = c_receiver.customer_id;


--Pattern: Same customer_id appearing in device_logins twice with different country_id within a short time window.


CREATE VIEW vw_impossible_travel AS
SELECT
    dl1.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    -- First login
    dl1.login_id          AS login_1_id,
    dl1.login_time        AS login_1_time,
    dl1.ip_address        AS login_1_ip,
    dl1.device_id         AS login_1_device,
    fc1.country_name      AS login_1_country,
    fc1.risk_level        AS login_1_country_risk,
    -- Second login
    dl2.login_id          AS login_2_id,
    dl2.login_time        AS login_2_time,
    dl2.ip_address        AS login_2_ip,
    dl2.device_id         AS login_2_device,
    fc2.country_name      AS login_2_country,
    fc2.risk_level        AS login_2_country_risk,
    -- Time between logins (minutes)
    EXTRACT(EPOCH FROM (dl2.login_time - dl1.login_time))/60 
        AS minutes_between_logins,
    CASE 
        WHEN dl1.country_id != dl2.country_id 
         AND EXTRACT(EPOCH FROM (dl2.login_time - dl1.login_time))/60 < 120
        THEN 'IMPOSSIBLE_TRAVEL'
        ELSE 'REVIEW'
    END AS travel_flag
FROM device_logins dl1
JOIN device_logins dl2 ON (
    dl1.customer_id = dl2.customer_id
    AND dl2.login_time > dl1.login_time
    AND dl2.login_time < dl1.login_time + INTERVAL '4 hours'
    AND dl1.country_id != dl2.country_id
)
JOIN customers c ON dl1.customer_id = c.customer_id
LEFT JOIN fatf_high_risk_countries fc1 
    ON dl1.country_id = fc1.country_id
LEFT JOIN fatf_high_risk_countries fc2 
    ON dl2.country_id = fc2.country_id;


--Pattern: branches + accounts + transactions + aml_alerts aggregated at branch_id level.

CREATE VIEW vw_branch_concentration_risk AS
SELECT
    br.branch_id,
    br.branch_name,
    br.city,
    br.state,
    -- Account stats
    COUNT(DISTINCT a.account_id)    AS total_accounts,
    COUNT(DISTINCT CASE WHEN a.status = 'ACTIVE' 
          THEN a.account_id END)    AS active_accounts,
    -- Transaction stats (last 30 days)
    COUNT(t.txn_id)                 AS total_txns_30d,
    SUM(t.amount)                   AS total_volume_30d,
    AVG(t.amount)                   AS avg_txn_amount_30d,
    MAX(t.amount)                   AS max_single_txn,
    -- High risk customer count
    COUNT(DISTINCT CASE WHEN c.risk_rating = 'HIGH' 
          THEN c.customer_id END)   AS high_risk_customers,
    -- Alert concentration
    COUNT(DISTINCT al.alert_id)     AS total_alerts_30d,
    COUNT(DISTINCT CASE WHEN al.severity = 'HIGH' 
          THEN al.alert_id END)     AS high_severity_alerts,
    -- CTR filings
    COUNT(DISTINCT cl.ctr_id)       AS ctr_filings_30d,
    SUM(cl.amount)                  AS ctr_reported_volume
FROM branches br
LEFT JOIN accounts a   ON br.branch_id = a.branch_id
LEFT JOIN customers c  ON a.customer_id = c.customer_id
LEFT JOIN transactions t ON (
    a.account_id = t.account_id
    AND t.txn_time >= CURRENT_TIMESTAMP - INTERVAL '30 days'
)
LEFT JOIN aml_alerts al ON (
    a.account_id = al.account_id
    AND al.created_at >= CURRENT_TIMESTAMP - INTERVAL '30 days'
)
LEFT JOIN ctr_log cl ON (
    a.account_id = cl.account_id
    AND cl.txn_time >= CURRENT_TIMESTAMP - INTERVAL '30 days'
)
GROUP BY br.branch_id, br.branch_name, br.city, br.state;


--Pattern: Account shows incoming credits → balance spikes → outgoing transfers → balance near zero. Detectable via balance_after_txn trajectory in transactions.

CREATE VIEW vw_mule_account_pattern AS
SELECT
    a.account_id,
    a.account_type,
    a.balance             AS current_balance,
    a.status              AS account_status,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    c.pan_number,
    -- Inflow stats
    COUNT(CASE WHEN t.txn_type IN ('CREDIT','IMPS_IN',
          'NEFT_IN','UPI_IN') THEN 1 END) AS inflow_count,
    SUM(CASE WHEN t.txn_type IN ('CREDIT','IMPS_IN',
        'NEFT_IN','UPI_IN') THEN t.amount ELSE 0 END) 
        AS total_inflow,
    -- Outflow stats
    COUNT(CASE WHEN t.txn_type IN ('DEBIT','IMPS_OUT',
          'NEFT_OUT','UPI_OUT') THEN 1 END) AS outflow_count,
    SUM(CASE WHEN t.txn_type IN ('DEBIT','IMPS_OUT',
        'NEFT_OUT','UPI_OUT') THEN t.amount ELSE 0 END) 
        AS total_outflow,
    -- Mule ratio: outflow/inflow should be ~1.0 for mules
    ROUND(
        SUM(CASE WHEN t.txn_type LIKE '%OUT%' OR t.txn_type = 'DEBIT' 
            THEN t.amount ELSE 0 END) /
        NULLIF(SUM(CASE WHEN t.txn_type LIKE '%IN%' OR t.txn_type = 'CREDIT' 
            THEN t.amount ELSE 0 END), 0)
    , 2) AS outflow_to_inflow_ratio,
    -- Balance volatility: mule accounts swing wildly
    MAX(t.balance_after_txn) - MIN(t.balance_after_txn) 
        AS balance_swing,
    MIN(t.balance_after_txn) AS minimum_balance_seen,
    COUNT(DISTINCT t.beneficiary_id) AS unique_beneficiaries,
    br.branch_name,
    br.city
FROM accounts a
JOIN customers c  ON a.customer_id = c.customer_id
JOIN branches br  ON a.branch_id = br.branch_id
JOIN transactions t ON (
    a.account_id = t.account_id
    AND t.txn_time >= CURRENT_TIMESTAMP - INTERVAL '30 days'
)
GROUP BY a.account_id, a.account_type, a.balance, a.status,
         c.customer_id, c.first_name, c.last_name,
         c.risk_rating, c.pan_number, br.branch_name, br.city;


--Pattern: customers.created_at is recent + accounts is new + high transaction volume immediately.


CREATE VIEW vw_new_account_fraud AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.created_at          AS customer_onboarded,
    (CURRENT_TIMESTAMP - c.created_at) 
        AS customer_age_days,
    c.risk_rating,
    c.pan_number,
    a.account_id,
    a.account_type,
    a.balance,
    a.status,
    k.status              AS kyc_status,
    -- Transaction behaviour since opening
    COUNT(t.txn_id)       AS total_txns,
    SUM(t.amount)         AS total_volume,
    MAX(t.amount)         AS largest_single_txn,
    COUNT(DISTINCT t.beneficiary_id) AS unique_beneficiaries,
    COUNT(DISTINCT t.channel) AS channels_used,
    -- Night transactions
    COUNT(CASE WHEN EXTRACT(HOUR FROM t.txn_time) 
               BETWEEN 23 AND 23 
               OR EXTRACT(HOUR FROM t.txn_time) BETWEEN 0 AND 4 
          THEN 1 END) AS night_txns,
    -- CTR immediately after opening
    COUNT(cl.ctr_id)      AS ctr_filings,
    -- AML alerts early
    COUNT(al.alert_id)    AS aml_alerts_raised
FROM customers c
JOIN accounts a      ON c.customer_id = a.customer_id
LEFT JOIN kyc_records k   ON c.customer_id = k.customer_id
LEFT JOIN transactions t  ON a.account_id = t.account_id
LEFT JOIN ctr_log cl      ON a.account_id = cl.account_id
LEFT JOIN aml_alerts al   ON a.account_id = al.account_id
WHERE c.created_at >= CURRENT_TIMESTAMP - INTERVAL '90 days'
GROUP BY c.customer_id, c.first_name, c.last_name,
         c.created_at, c.risk_rating, c.pan_number,
         a.account_id, a.account_type, a.balance, a.status,
         k.status;


--Pattern: Multiple account_id values in beneficiaries sharing the same beneficiary_account_number.


CREATE VIEW vw_shared_beneficiary_network AS
SELECT
    b.beneficiary_account_number,
    b.beneficiary_name,
    -- How many different source accounts use this beneficiary?
    COUNT(DISTINCT b.account_id)    AS source_account_count,
    COUNT(DISTINCT a.customer_id)   AS unique_customers_sending,
    -- Transaction stats to this beneficiary
    COUNT(t.txn_id)                 AS total_txns_received,
    SUM(t.amount)                   AS total_received,
    MAX(t.amount)                   AS largest_single_receipt,
    MIN(t.txn_time)                 AS first_txn,
    MAX(t.txn_time)                 AS latest_txn,
    -- Risk aggregation of senders
    COUNT(DISTINCT CASE WHEN c.risk_rating = 'HIGH' 
          THEN c.customer_id END)   AS high_risk_senders,
    -- Country risk of beneficiary
    fc.country_name,
    fc.risk_level,
    fc.fatf_list_type,
    -- Collect list of sending customers
    STRING_AGG(DISTINCT c.first_name || ' ' || c.last_name, 
               ', ')                AS sending_customers
FROM beneficiaries b
JOIN accounts a  ON b.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
LEFT JOIN transactions t   ON b.beneficiary_id = t.beneficiary_id
LEFT JOIN fatf_high_risk_countries fc ON b.country_id = fc.country_id
GROUP BY b.beneficiary_account_number, b.beneficiary_name,
         fc.country_name, fc.risk_level, fc.fatf_list_type
HAVING COUNT(DISTINCT b.account_id) > 1;


--Pattern: aml_alerts.status = 'OPEN' + created_at is old = SLA breach risk.


CREATE VIEW vw_alert_aging_sla AS
SELECT
    al.alert_id,
    al.alert_type,
    al.severity,
    al.status,
    al.created_at         AS alert_raised_at,
    -- Age of alert
    (CURRENT_TIMESTAMP - al.created_at) 
        AS alert_age_days,
    -- SLA breach classification
    CASE 
        WHEN (CURRENT_TIMESTAMP - al.created_at) > INTERVAL '45 days' 
             AND al.severity = 'HIGH'   THEN 'CRITICAL_BREACH'
        WHEN (CURRENT_TIMESTAMP - al.created_at) > INTERVAL '30 days' 
             AND al.severity = 'HIGH'   THEN 'HIGH_BREACH'
        WHEN (CURRENT_TIMESTAMP - al.created_at) > INTERVAL '60 days' 
             THEN 'STANDARD_BREACH'
        ELSE 'WITHIN_SLA'
    END AS sla_status,
    a.account_id,
    a.account_type,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_rating,
    t.txn_id,
    t.amount,
    t.txn_time,
    t.txn_type,
    br.branch_name,
    br.city
FROM aml_alerts al
JOIN accounts a  ON al.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN branches br ON a.branch_id = br.branch_id
LEFT JOIN transactions t ON al.txn_id = t.txn_id
WHERE al.status = 'OPEN'
ORDER BY alert_age_days DESC;