import sys
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def predict_risk(data):
    training_data = {
        "income": [20000, 50000, 80000, 30000, 100000, 15000, 60000, 40000, 90000, 25000],
        "loan_amount": [50000, 200000, 500000, 100000, 800000, 50000, 300000, 150000, 600000, 80000],
        "credit_history": [6, 24, 60, 12, 48, 3, 36, 18, 50, 8],
        "target": [0, 1, 1, 0, 1, 0, 1, 1, 1, 0]
    }
    
    df = pd.DataFrame(training_data)
    X = df[["income", "loan_amount", "credit_history"]]
    y = df["target"]
    
    clf = RandomForestClassifier(n_estimators=10, random_state=42)
    clf.fit(X, y)
    
    income = data.get("income", 0)
    loan_amount = data.get("loan_amount", 0)
    credit_history = data.get("credit_history_months", 12)
    
    input_df = pd.DataFrame([[income, loan_amount, credit_history]], 
                            columns=["income", "loan_amount", "credit_history"])
    
    prob_default = clf.predict_proba(input_df)[0][0]
    
    decision = "MANUAL_REVIEW"
    max_eligible_amount = 0
    
    if prob_default > 0.50:
        decision = "REJECTED"
        max_eligible_amount = 0
    elif prob_default < 0.20:
        decision = "APPROVED"
        max_eligible_amount = income * 15
    else:
        decision = "MANUAL_REVIEW"
        max_eligible_amount = income * 5
        
    return {
        "risk_score": round(1 - prob_default, 2),
        "decision": decision,
        "max_eligible_amount": max_eligible_amount,
        "default_probability": round(prob_default, 2)
    }

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            input_json = ' '.join(sys.argv[1:])
            data = json.loads(input_json)
            result = predict_risk(data)
            print(json.dumps(result))
        else:
            print(json.dumps({"error": "No input provided"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))