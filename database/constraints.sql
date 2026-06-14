-- ==============================================================================
-- constraint.sql
-- Description: Foreign key relationships and data integrity constraints.
-- ==============================================================================

-- Foreign Key Constraints
ALTER TABLE accounts 
    ADD CONSTRAINT fk_accounts_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    ADD CONSTRAINT fk_accounts_branch FOREIGN KEY (branch_id) REFERENCES branches(branch_id);

ALTER TABLE kyc_records
    ADD CONSTRAINT fk_kyc_customer
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id);

ALTER TABLE kyc_records
    ADD CONSTRAINT uq_kyc_customer
    UNIQUE (customer_id);


ALTER TABLE beneficiaries 
    ADD CONSTRAINT fk_beneficiaries_account FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    ADD CONSTRAINT fk_beneficiaries_country FOREIGN KEY (country_id) REFERENCES fatf_high_risk_countries(country_id);

ALTER TABLE device_logins 
    ADD CONSTRAINT fk_device_logins_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    ADD CONSTRAINT fk_device_logins_country FOREIGN KEY (country_id) REFERENCES fatf_high_risk_countries(country_id);

ALTER TABLE transactions 
    ADD CONSTRAINT fk_txn_account FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    ADD CONSTRAINT fk_txn_beneficiary FOREIGN KEY (beneficiary_id) REFERENCES beneficiaries(beneficiary_id),
    ADD CONSTRAINT fk_txn_country FOREIGN KEY (country_id) REFERENCES fatf_high_risk_countries(country_id);

ALTER TABLE aml_alerts 
    ADD CONSTRAINT fk_aml_account FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    ADD CONSTRAINT fk_aml_txn FOREIGN KEY (txn_id) REFERENCES transactions(txn_id);

ALTER TABLE ctr_log 
    ADD CONSTRAINT fk_ctr_account FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    ADD CONSTRAINT fk_ctr_txn FOREIGN KEY (txn_id) REFERENCES transactions(txn_id);

-- Check Constraints for Data Integrity
ALTER TABLE customers
    ADD CONSTRAINT chk_customer_no_space
        CHECK(customer_id !~ '\s'),

    ADD CONSTRAINT chk_customer_only_number
        CHECK (
            phone_number ~ '^[0-9]{10}$' AND
            aadhar ~ '^[0-9]{12}$'
        ),

    ADD CONSTRAINT chk_pan_valid
        CHECK (
            pan_number ~ '^[A-Z]{5}[0-9]{4}[A-Z]$'
        );

ALTER TABLE branches
    ADD CONSTRAINT chk_branch_id_valid
        CHECK(
            branch_id ~ '[A-Z]{4}0[A-Z0-9]{6}$'
        ),
    ADD CONSTRAINT chk_branch_only_alphabet
        CHECK (
            branch_name ~ '^[A-Za-z ]+$' AND
            city ~ '^[A-Za-z ]+$' AND
            state ~ '^[A-Za-z ]+$'
        );
ALTER TABLE fatf_high_risk_countries
    ADD CONSTRAINT chk_countries_only_alphabet
        CHECK (
            country_name ~ '^[A-Za-z ]+$' AND
            iso_country_code ~ '^[A-Za-z]+$' AND
            risk_level ~ '^[A-Za-z]+$'
            
        ),
    ADD CONSTRAINT chk_risk_score 
        CHECK (
            risk_score >= 0
    );

ALTER TABLE accounts
    ADD CONSTRAINT chk_accounts_no_space
        CHECK(account_id !~ '\s' AND
         customer_id !~ '\s' ),

    ADD CONSTRAINT chk_accounts_id_valid
        CHECK(
            branch_id ~ '[A-Z]{4}0[A-Z0-9]{6}$'
        ),

    ADD CONSTRAINT chk_accounts_only_alphabet
        CHECK (
            account_type ~ '^[A-Za-z]+$' AND
            status ~ '^[A-Za-z]+$'
           
        );

ALTER TABLE kyc_records
    ADD CONSTRAINT chk_kyc_no_space
        CHECK(
         customer_id !~ '\s' 
        ),
    ADD CONSTRAINT chk_kyc_only_alphabet
        CHECK (
            status ~ '^[A-Za-z]+$'
           
        );

ALTER TABLE beneficiaries
    ADD CONSTRAINT chk_beneficiaries_no_space
        CHECK(
            account_id !~ '\s'
            AND
            beneficiary_account_number !~ '\s'
        );

ALTER TABLE device_logins
    ADD CONSTRAINT chk_device_login_no_space
        CHECK(customer_id !~ '\s' AND
        device_id !~ '\s' AND
        ip_address !~ '\s');
    

    
ALTER TABLE transactions 
    ADD CONSTRAINT chk_txn_amount CHECK (amount >= 0),
     ADD CONSTRAINT chk_txn_no_space
        CHECK(account_id !~ '\s'
        );

ALTER TABLE ctr_log 
    ADD CONSTRAINT chk_ctr_amount CHECK (amount >= 0);