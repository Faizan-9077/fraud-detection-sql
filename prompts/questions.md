# Bank AML Database - Few-Shot Text-to-SQL Prompts

## System Prompt Context

You are an expert PostgreSQL database developer. Your job is to convert natural language queries from compliance officers into optimized, executable SQL queries. Use standard PostgreSQL syntax (e.g., `TIMESTAMPTZ`, `CURRENT_DATE`, `INTERVAL`).

---

## 1. Basic Lookups (Simple SELECT & WHERE)

**Question:** Get the customer details for the user with the email `johndoe@example.com`.

```sql
SELECT customer_id, first_name, last_name, phone_number, risk_rating
FROM customers
WHERE email = 'johndoe@example.com';
```

---

## 2. Basic Filtering (AND/OR)

**Question:** List all active accounts that have a balance greater than 100,000 INR.

```sql
SELECT account_id, customer_id, branch_id, balance
FROM accounts
WHERE status = 'ACTIVE'
  AND balance > 100000;
```

---

## 3. Aggregation (GROUP BY & COUNT)

**Question:** Count the total number of customers in each risk rating category.

```sql
SELECT risk_rating, COUNT(customer_id) AS total_customers
FROM customers
GROUP BY risk_rating
ORDER BY total_customers DESC;
```

---

## 4. Aggregation (SUM with JOIN)

**Question:** What is the total combined account balance for the customer with cif_no `CIF`?

```sql
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       SUM(a.balance) AS total_balance
FROM customers c
JOIN accounts a
  ON c.customer_id = a.customer_id
WHERE c.customer_id = 'CIF'
GROUP BY c.customer_id, c.first_name, c.last_name;
```

---

## 5. Multi-Table Joins (3 Tables)

**Question:** Show me all recent transactions made by customers who have a `HIGH` risk rating.

```sql
SELECT t.txn_id,
       t.txn_time,
       t.amount,
       t.txn_type,
       c.first_name,
       c.last_name
FROM transactions t
JOIN accounts a
  ON t.account_id = a.account_id
JOIN customers c
  ON a.customer_id = c.customer_id
WHERE c.risk_rating = 'HIGH'
ORDER BY t.txn_time DESC
LIMIT 100;
```

---

## 6. Left Join & Null Checking (Data Anomalies)

**Question:** Find all customers who have registered an account but KYC has been rejected.

```sql
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       c.created_at
FROM customers c
LEFT JOIN kyc_records k
  ON c.customer_id = k.customer_id
WHERE k.status = 'REJECTED';
```

---

## 7. Time-Interval Filtering (Recent Activity)

**Question:** Retrieve all AML alerts that were generated in the last 7 days and are still in `OPEN` status.

```sql
SELECT alert_id,
       account_id,
       txn_id,
       alert_type,
       severity
FROM aml_alerts
WHERE status = 'OPEN'
  AND created_at >= NOW() - INTERVAL '7 days';
```

---

## 8. Domain Specific Filtering (CTR / Large Transactions)

**Question:** Find all cash transactions (credits or debits) over 10,000 logged in the CTR table for this month.

```sql
SELECT ctr_id,
       account_id,
       txn_id,
       amount,
       txn_time
FROM ctr_log
WHERE amount > 10000
  AND DATE_TRUNC('month', txn_time) = DATE_TRUNC('month', CURRENT_DATE);
```

---

## 9. Relational Lookups (Geographic Risk)

**Question:** Give me a list of customers who logged in from a country with a FATF risk score higher than 75.

```sql
SELECT DISTINCT c.customer_id,
       c.first_name,
       c.last_name,
       f.country_name,
       f.risk_score
FROM device_logins d
JOIN customers c
  ON d.customer_id = c.customer_id
JOIN fatf_high_risk_countries f
  ON d.country_id = f.country_id
WHERE f.risk_score > 75;
```

---

## 10. Nested Subqueries (Highest Value)

**Question:** Which branch has the account with the single highest balance in the bank?

```sql
SELECT b.branch_id,
       b.branch_name,
       b.city,
       a.balance,
       a.account_id
FROM branches b
JOIN accounts a
  ON b.branch_id = a.branch_id
WHERE a.balance = (
    SELECT MAX(balance)
    FROM accounts
);
```

---

## 11. String Manipulation & Pattern Matching (LIKE)

**Question:** Find all beneficiaries whose name contains the word `alex` or `raman`.

```sql
SELECT beneficiary_id,
       account_id,
       beneficiary_name,
       beneficiary_account_number
FROM beneficiaries
WHERE beneficiary_name ILIKE '%alex%'
   OR beneficiary_name ILIKE '%raman%';
```

---

## 12. Cross-Border AML Rule (High-Risk Beneficiary)

**Question:** Show all outward (`DEBIT`) transactions sent to beneficiaries located in countries marked as FATF list type `BLACK`.

```sql
SELECT t.txn_id,
       t.account_id,
       t.amount,
       b.beneficiary_name,
       f.country_name
FROM transactions t
JOIN beneficiaries b
  ON t.beneficiary_id = b.beneficiary_id
JOIN fatf_high_risk_countries f
  ON b.country_id = f.country_id
WHERE t.txn_type = 'CASH_WITHDRAWAL'
  AND f.fatf_list_type = 'BLACK';
```

---

## 13. HAVING Clause (Velocity Rule)

**Question:** Identify accounts that had more than 10 outgoing transactions in a single day.

```sql
SELECT account_id,
       DATE(txn_time) AS txn_date,
       COUNT(txn_id) AS total_txns,
       SUM(amount) AS total_volume
FROM transactions
WHERE txn_type = 'CASH_WITHDRAWAL'
GROUP BY account_id, DATE(txn_time)
HAVING COUNT(txn_id) > 10
ORDER BY total_txns DESC;
```

---

## 14. AML Structuring / Smurfing Rule

**Question:** Find accounts that made 3 or more deposits (`CREDIT`) sized between 9,000 and 9,999 within the last 5 days.

```sql
SELECT account_id,
       COUNT(txn_id) AS smurf_attempts,
       SUM(amount) AS total_smurfed
FROM transactions
WHERE txn_type = 'CASH_DEPOSIT'
  AND amount BETWEEN 9000 AND 9999
  AND txn_time >= NOW() - INTERVAL '5 days'
GROUP BY account_id
HAVING COUNT(txn_id) >= 3;
```

---

## 15. Advanced Aggregation (Total At-Risk Amount)

**Question:** Generate a summary showing the total number of open AML alerts and the total transaction amount associated with those alerts, grouped by severity.

```sql
SELECT aml.severity,
       COUNT(aml.alert_id) AS total_alerts,
       SUM(t.amount) AS total_risk_amount
FROM aml_alerts aml
JOIN transactions t
  ON aml.txn_id = t.txn_id
WHERE aml.status = 'OPEN'
GROUP BY aml.severity;
```

---

## 16. Window Functions (Latest Record per Group)

**Question:** Get the most recent login IP address and device ID for every customer.

```sql
WITH RankedLogins AS (
    SELECT customer_id,
           ip_address,
           device_id,
           login_time,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id
               ORDER BY login_time DESC
           ) AS rn
    FROM device_logins
)
SELECT customer_id,
       ip_address,
       device_id,
       login_time
FROM RankedLogins
WHERE rn = 1;
```

---

## 17. CTEs (Pass-Through Account Detection)

**Question:** Find accounts that received more than 50,000 in credits today and have already debited out more than 90% of that credited amount today.

```sql
WITH DailyTotals AS (
    SELECT account_id,
           SUM(CASE WHEN txn_type = 'CASH_DEPOSIT' THEN amount ELSE 0 END) AS total_in,
           SUM(CASE WHEN txn_type = 'CASH_WITHDRAWAL' THEN amount ELSE 0 END) AS total_out
    FROM transactions
    WHERE DATE(txn_time) = CURRENT_DATE
    GROUP BY account_id
)
SELECT account_id,
       total_in,
       total_out
FROM DailyTotals
WHERE total_in > 50000
  AND total_out >= (total_in * 0.90);
```

---

## 18. Self-Joins (Impossible Travel Rule)

**Question:** Identify customers who logged in from two completely different countries within a 12-hour window.

```sql
SELECT DISTINCT d1.customer_id,
       d1.login_time AS first_login,
       d1.country_id AS first_country,
       d2.login_time AS second_login,
       d2.country_id AS second_country
FROM device_logins d1
JOIN device_logins d2
  ON d1.customer_id = d2.customer_id
 AND d1.login_id <> d2.login_id
WHERE d1.country_id <> d2.country_id
  AND d2.login_time > d1.login_time
  AND d2.login_time <= d1.login_time + INTERVAL '12 hours';
```

---

## 19. Full 360° Account View

**Question:** Retrieve a full profile for account `ACC-12345`, showing customer name, current balance, branch city, and the date of their last KYC review.

```sql
SELECT a.account_id,
       c.first_name,
       c.last_name,
       a.balance,
       b.city AS branch_city,
       k.review_date AS last_kyc_review
FROM accounts a
JOIN customers c
  ON a.customer_id = c.customer_id
JOIN branches b
  ON a.branch_id = b.branch_id
LEFT JOIN kyc_records k
  ON c.customer_id = k.customer_id
WHERE a.account_id = 'ACC-12345'
ORDER BY k.review_date DESC
LIMIT 1;
```

---

## 20. Advanced Window Functions (Running Balance / Audit Trail)

**Question:** Show the transaction history for account `ACC-9988`, including a calculated running balance after each transaction chronologically.

```sql
SELECT txn_id,
       txn_time,
       txn_type,
       amount,
       SUM(
           CASE
               WHEN txn_type = 'CREDIT' THEN amount
               ELSE -amount
           END
       ) OVER (
           ORDER BY txn_time ASC
       ) AS calculated_running_balance,
       balance_after_txn AS system_recorded_balance
FROM transactions
WHERE account_id = 'ACC-9988'
ORDER BY txn_time ASC;
```
