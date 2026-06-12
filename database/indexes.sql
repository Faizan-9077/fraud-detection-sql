-- ==============================================================================
-- indexes.sql
-- Description: Indexes for foreign keys and frequently queried columns 
--              to optimize reporting and transactional lookups.
-- ==============================================================================

-- Foreign Key Indexes (Crucial for JOIN performance and cascade operations)
CREATE INDEX idx_accounts_customer_id ON accounts(customer_id);
CREATE INDEX idx_accounts_branch_id ON accounts(branch_id);
CREATE INDEX idx_kyc_customer_id ON kyc_records(customer_id);
CREATE INDEX idx_beneficiaries_account_id ON beneficiaries(account_id);
CREATE INDEX idx_beneficiaries_country_id ON beneficiaries(country_id);
CREATE INDEX idx_device_logins_customer_id ON device_logins(customer_id);
CREATE INDEX idx_device_logins_country_id ON device_logins(country_id);
CREATE INDEX idx_transactions_account_id ON transactions(account_id);
CREATE INDEX idx_transactions_beneficiary_id ON transactions(beneficiary_id);
CREATE INDEX idx_transactions_country_id ON transactions(country_id);
CREATE INDEX idx_aml_alerts_account_id ON aml_alerts(account_id);
CREATE INDEX idx_aml_alerts_txn_id ON aml_alerts(txn_id);
CREATE INDEX idx_ctr_log_account_id ON ctr_log(account_id);
CREATE INDEX idx_ctr_log_txn_id ON ctr_log(txn_id);

-- Operational & Analytical Lookups (Filtering/Sorting)
CREATE INDEX idx_customers_risk_rating ON customers(risk_rating);
CREATE INDEX idx_accounts_status ON accounts(status);
CREATE INDEX idx_transactions_txn_time ON transactions(txn_time DESC);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_device_id ON transactions(device_id);
CREATE INDEX idx_aml_alerts_status_severity ON aml_alerts(status, severity);
CREATE INDEX idx_aml_alerts_created_at ON aml_alerts(created_at DESC);
CREATE INDEX idx_device_logins_ip_device ON device_logins(ip_address, device_id);
CREATE INDEX idx_device_logins_time ON device_logins(login_time DESC);