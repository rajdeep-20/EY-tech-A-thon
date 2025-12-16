import sys
import json

def verify_user(data):
    income = data.get("income", 0)
    pan = data.get("pan", "")
    
    # Rule 1: Minimum Income Check
    if income < 20000:
        return {
            "status": "REJECTED",
            "reason": "Low Income",
            "credit_score": 0,
            "eligible_amount": 0
        }
        
    # Rule 2: Credit Score Simulation based on PAN
    if pan.strip().upper().endswith('F'):
        credit_score = 450
        risk_level = "HIGH"
        status = "REJECTED"
        reason = "Low Credit Score"
        eligible_amount = 0
    else:
        credit_score = 750 + (income // 10000) # Bonus for higher income
        risk_level = "LOW"
        status = "APPROVED"
        reason = "Good Credit History"
        eligible_amount = income * 10 # 10x monthly income
        
    return {
        "status": status,
        "reason": reason,
        "credit_score": credit_score,
        "risk_level": risk_level,
        "eligible_amount": eligible_amount
    }

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            input_json = sys.argv[1]
            data = json.loads(input_json)
            result = verify_user(data)
            print(json.dumps(result))
        else:
            print(json.dumps({"error": "No input provided"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
