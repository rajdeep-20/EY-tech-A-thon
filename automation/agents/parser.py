import sys
import json
import re
import ast
import os

def parse_money(text):
    """Parses money strings like '50k', '5 lakhs', '50,000' into integers."""
    text = text.lower().replace(',', '')
    multiplier = 1
    if 'k' in text:
        multiplier = 1000
        text = text.replace('k', '')
    elif 'lakh' in text:
        multiplier = 100000
        text = text.replace('lakhs', '').replace('lakh', '')
    elif 'cr' in text or 'crore' in text:
        multiplier = 10000000
        text = text.replace('crores', '').replace('crore', '').replace('cr', '')
        
    match = re.search(r"(\d+(\.\d+)?)", text)
    if match:
        return int(float(match.group(1)) * multiplier)
    return None

def parse_input(text):
    data = {}
    
    # Extract Name
    # Look for "My name is X", "I am X", or just capitalized words at start if short
    name_match = re.search(r"(?:my name is|i am|name is)\s+([a-zA-Z\s]+)", text, re.IGNORECASE)
    if name_match:
        data["name"] = name_match.group(1).strip()
    else:
        # Fallback: if text is short and starts with a name-like pattern
        words = text.split()
        if len(words) > 0 and words[0][0].isupper() and len(words) < 5:
             data["name"] = words[0]

    # Extract Income
    # Patterns: "income 50k", "earn 50000", "salary 5 lakhs"
    income_match = re.search(r"(?:income|earn|salary).*?([\d,]+(?:\s*(?:k|lakhs?|cr|crores?))?)", text, re.IGNORECASE)
    if income_match:
        val = parse_money(income_match.group(1))
        if val: data["income"] = val
        
    # Extract Loan Amount
    # Patterns: "loan 200000", "need 50k", "amount 5 lakhs"
    loan_match = re.search(r"(?:loan|amount|need|want).*?([\d,]+(?:\s*(?:k|lakhs?|cr|crores?))?)", text, re.IGNORECASE)
    if loan_match:
        val = parse_money(loan_match.group(1))
        if val: data["loan_amount"] = val

    # Extract PAN Number (ABCDE1234F)
    pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]{1}", text, re.IGNORECASE)
    if pan_match:
        data["pan_number"] = pan_match.group(0).upper()

    # Extract Employment Type
    if re.search(r"business|self[- ]?employed", text, re.IGNORECASE):
        data["employment_type"] = "Business"
    elif re.search(r"salaried|job|work", text, re.IGNORECASE):
        data["employment_type"] = "Salaried"
    else:
        # Default if not found but income exists, assume salaried for safety or leave empty
        if "income" in data:
            data["employment_type"] = "Salaried"
        
    # Determine Intent
    if "loan" in text.lower() or "money" in text.lower() or "amount" in text.lower():
        data["intent"] = "loan_application"
    else:
        data["intent"] = "general_inquiry"
        
    return data

if __name__ == "__main__":
    try:
        input_str = ""
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if os.path.exists(arg) and os.path.isfile(arg):
                with open(arg, 'r') as f:
                    input_str = f.read().strip()
            else:
                input_str = ' '.join(sys.argv[1:])
        else:
            input_str = sys.stdin.read().strip()

        # Try to interpret as python literal (e.g. string with quotes), else treat as raw string
        try:
            text = ast.literal_eval(input_str)
            if not isinstance(text, str):
                text = input_str # Fallback if it evaluates to something else
        except:
            text = input_str
            
        result = parse_input(text)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))