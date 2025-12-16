# Sample Loan Documents

This directory contains sample PDF documents to test the Loan Assistant's file upload and verification flow.

**Note:** The current system uses the **Chat Input** to determine the loan amount and income for risk assessment. The uploaded file is required for the process but its content is not currently parsed for the decision logic.

## How to Simulate Scenarios

### 1. Accepted Loan Scenario
To verify a successful loan application (Sanction Letter Generation):

1.  **Chat Input**: Type the following (High Income / Reasonable Loan Amount):
    > "My name is Rajdeep and I need a loan of 50000"
    *(This implies a default income of 50,000 if not specified, resulting in a good debt-to-income ratio)*

2.  **Upload**: Select `Accepted_Loan_Profile.pdf` when prompted.

3.  **Outcome**: The system should approve the loan and provide a Sanction Letter.

### 2. Rejected Loan Scenario
To verify a rejected loan application:

1.  **Chat Input**: Type the following (High Loan Amount vs Default Income):
    > "My name is John and I need a loan of 5000000"
    *(50 Lakhs loan with default income of 50k results in a very high risk)*

2.  **Upload**: Select `Rejected_Loan_Profile.pdf` when prompted.

3.  **Outcome**: The system should reject the loan based on the high risk assessment.
