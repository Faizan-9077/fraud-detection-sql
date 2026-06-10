# Fraud Detection & Compliance Reporting Dataset Design

## Project Overview

This project simulates a banking environment for an AI-powered fraud detection and compliance reporting system.

The generated dataset will be used for:

* Fraud Detection
* AML (Anti-Money Laundering) Analysis
* Compliance Reporting
* Natural Language to SQL using LLaMA 3
* Risk Investigation
* SAR (Suspicious Activity Report) Generation

Target:

* Around 500,000 transactions
* Embedded fraud patterns
* Deterministic data generation using random seeds

---

# Database Relationship Diagram

```
Customers
    |
    +------ Accounts
    |            |
    |            +------ Transactions
    |            |
    |            +------ Beneficiaries
    |            |
    |            +------ AML Alerts
    |            |
    |            +------ CTR Log
    |
    +------ Device Logins
    |
    +------ KYC Records

Branches

FATF High Risk Countries
        |
        +------ Transactions
        +------ Beneficiaries
```

---

# Table Design

## 1. Customers

Purpose:
Store customer master information.

Rows: 50,000

Primary Key:

* customer_id

Columns:

* customer_id
* full_name
* gender
* date_of_birth
* phone
* email
* address
* occupation
* annual_income
* risk_rating
* created_at

---

## 2. Accounts

Purpose:
Store bank accounts belonging to customers.

Rows: 100,000

Primary Key:

* account_id

Foreign Keys:

* customer_id → Customers
* branch_id → Branches

Columns:

* account_id
* customer_id
* branch_id
* account_type
* balance
* status
* opened_at

---

## 3. Transactions

Purpose:
Store all financial transactions.

Rows: 500,000

Primary Key:

* transaction_id

Foreign Keys:

* account_id → Accounts
* beneficiary_id → Beneficiaries

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

## 4. Beneficiaries

Purpose:
Store beneficiary account details.

Rows: 150,000

Primary Key:

* beneficiary_id

Foreign Key:

* account_id → Accounts

Columns:

* beneficiary_id
* account_id
* beneficiary_name
* bank_name
* country_code

---

## 5. Device Logins

Purpose:
Track customer login activities.

Rows: 300,000

Primary Key:

* login_id

Foreign Key:

* customer_id → Customers

Columns:

* login_id
* customer_id
* device_id
* ip_address
* login_time
* country

---

## 6. KYC Records

Purpose:
Store customer verification details.

Rows: 50,000

Primary Key:

* kyc_id

Foreign Key:

* customer_id → Customers

Columns:

* kyc_id
* customer_id
* kyc_status
* document_type
* verification_date

---

## 7. AML Alerts

Purpose:
Store suspicious activity alerts.

Rows: 10,000

Primary Key:

* alert_id

Foreign Key:

* transaction_id → Transactions

Columns:

* alert_id
* transaction_id
* alert_type
* risk_score
* created_at

---

## 8. CTR Log

Purpose:
Store Currency Transaction Reports.

Rows: 5,000

Primary Key:

* ctr_id

Foreign Key:

* transaction_id → Transactions

Columns:

* ctr_id
* transaction_id
* reported_amount
* report_date

---

## 9. Branches

Purpose:
Store bank branch information.

Rows: 100

Primary Key:

* branch_id

Columns:

* branch_id
* branch_name
* city
* state
* country

---

## 10. FATF High Risk Countries

Purpose:
Store high-risk countries for AML monitoring.

Rows: 20

Primary Key:

* country_code

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

Minimum Amount:
₹100

Maximum Amount:
₹10,00,000

---

# Planned Fraud Patterns

## Pattern 1

Structuring

* Five transactions below ₹2,00,000 within 72 hours

## Pattern 2

Dormant Account Reactivation

* No activity for six months followed by a large transfer

## Pattern 3

Night Transactions

* Between 11 PM and 4 AM

## Pattern 4

High-Risk FATF Country Transactions

## Pattern 5

Rapid Beneficiary Addition

## Pattern 6

Multiple Device Logins

## Pattern 7

Large Round Amount Transfers

## Pattern 8

Repeated Failed Transactions

---

# Data Generation Order

1. Branches
2. FATF High Risk Countries
3. Customers
4. KYC Records
5. Accounts
6. Beneficiaries
7. Transactions
8. Device Logins
9. AML Alerts
10. CTR Log

---

# Development Workflow

Data Generation
|
V
CSV Files
|
V
PostgreSQL Database
|
V
LLaMA 3 NL to SQL
|
V
Fraud Investigation UI
|
V
SAR Evidence Generation

---

# Week 1 Deliverables

* schema.sql
* generate_data.py
* question_bank.md
* LLaMA 3 API connectivity

---

# Notes

* Data generation must be deterministic.
* Random seeds should be fixed.
* Fraud patterns must be embedded intentionally.
* Generated data should support natural language fraud investigation queries.
* All generated data should be compatible with PostgreSQL schema.
