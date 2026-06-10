# Fraud Detection Dataset Design

## Customers

Rows: 50,000

Columns:

* customer_id
* full_name
* phone
* email
* address
* risk_rating
* created_at

---

## Accounts

Rows: 100,000

Columns:

* account_id
* customer_id
* branch_id
* account_type
* balance
* status
* opened_at

---

## Transactions

Rows: 500,000

Columns:

* transaction_id
* account_id
* beneficiary_id
* amount
* transaction_type
* transaction_time
* country_code
* status

---

## Beneficiaries

Rows: 150,000

Columns:

* beneficiary_id
* account_id
* beneficiary_name
* bank_name
* country_code

---

## Device Logins

Rows: 300,000

Columns:

* login_id
* customer_id
* device_id
* ip_address
* login_time
* country

---

## KYC Records

Rows: 50,000

Columns:

* kyc_id
* customer_id
* kyc_status
* document_type
* verification_date

---

## AML Alerts

Rows: 10,000

Columns:

* alert_id
* transaction_id
* alert_type
* risk_score
* created_at

---

## CTR Log

Rows: 5,000

Columns:

* ctr_id
* transaction_id
* reported_amount
* report_date

---

## Branches

Rows: 100

Columns:

* branch_id
* branch_name
* city
* state
* country

---

## FATF High Risk Countries

Rows: 20

Columns:

* country_code
* country_name
* risk_level


---

# Data Generation Rules

## Customer Risk Distribution

| Risk Rating | Percentage |
| ----------- | ---------- |
| LOW         | 80%        |
| MEDIUM      | 15%        |
| HIGH        | 5%         |

---

## Account Type Distribution

| Account Type | Percentage |
| ------------ | ---------- |
| Savings      | 60%        |
| Current      | 25%        |
| Salary       | 15%        |

---

## Transaction Types

* Deposit
* Withdrawal
* Transfer
* UPI
* NEFT
* RTGS
* IMPS

---

## Transaction Amount Range

Minimum Amount: ₹100

Maximum Amount: ₹10,00,000

---

## Planned Fraud Patterns

1. Structuring

   * 5 transactions below ₹2,00,000 within 72 hours

2. Dormant Account Reactivation

   * No activity for 6 months followed by a large transfer

3. Night Transactions

   * Between 11 PM and 4 AM

4. High-Risk FATF Country Transactions

5. Rapid Beneficiary Addition

6. Multiple Device Logins

7. Large Round Amount Transfers

8. Repeated Failed Transactions

---

## Data Generation Order

1. Branches
2. Customers
3. KYC Records
4. Accounts
5. Beneficiaries
6. Transactions
7. Device Logins
8. AML Alerts
9. CTR Log
