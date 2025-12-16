import sys
import json
import os

# Define output file for debug
DEBUG_FILE = "debug_risk.json"

def log_error(e):
    err_res = {"error": str(e)}
    try:
        with open(DEBUG_FILE, "w") as f:
            json.dump(err_res, f)
    except:
        pass
    print(json.dumps(err_res))

try:
    # Suppress TensorFlow logs
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    
    # Redirect stderr to null
    sys.stderr = open(os.devnull, 'w')

    import ast
    import pandas as pd
    import numpy as np
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    DATA_FILE = "loan_data_synthetic.csv"

    def generate_synthetic_data():
        np.random.seed(42)
        n_samples = 1000
        
        income = np.random.randint(20000, 150000, n_samples)
        loan_amount = np.random.randint(50000, 1000000, n_samples)
        credit_score = np.random.randint(300, 900, n_samples)
        employment_status = np.random.randint(0, 2, n_samples)
        
        logits = (
            - (income / 100000) * 2 
            + (loan_amount / 200000) * 1.5 
            - (credit_score / 100) * 1.5 
            - employment_status * 1.0
            + 2.0
        )
        default_prob = 1 / (1 + np.exp(-logits))
        defaults = (np.random.rand(n_samples) < default_prob).astype(int)
        
        df = pd.DataFrame({
            "income": income,
            "loan_amount": loan_amount,
            "credit_score": credit_score,
            "employment_status": employment_status,
            "default_label": defaults
        })
        
        df.to_csv(DATA_FILE, index=False)

    def train_and_predict(input_data):
        if not os.path.exists(DATA_FILE):
            generate_synthetic_data()
            
        df = pd.read_csv(DATA_FILE)
        
        X = df[["income", "loan_amount", "credit_score", "employment_status"]]
        y = df["default_label"]
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        model = keras.Sequential([
            layers.Dense(16, activation='relu', input_shape=(X_scaled.shape[1],)),
            layers.Dense(8, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        model.fit(X_scaled, y, epochs=5, verbose=0, batch_size=32)
        
        income = input_data.get("income", 50000)
        loan_amount = input_data.get("loan_amount", 200000)
        credit_score = input_data.get("credit_score", 700)
        employment_status = 1 if str(input_data.get("employment_type", "")).lower() == "salaried" else 0
        
        input_features = np.array([[income, loan_amount, credit_score, employment_status]])
        input_scaled = scaler.transform(input_features)
        
        risk_prob = model.predict(input_scaled, verbose=0)[0][0]
        
        risk_score = 1 - risk_prob
        decision = "APPROVED" if risk_prob < 0.4 else "REJECTED"
        confidence = float(max(risk_prob, 1 - risk_prob))
        
        res = {
            "risk_score": round(float(risk_score), 2),
            "decision": decision,
            "confidence": round(confidence, 2),
            "default_probability": round(float(risk_prob), 2),
            "max_eligible_amount": int(income * 10) if decision == "APPROVED" else 0 # Add max_eligible_amount
        }
        
        # Write success to debug file
        with open(DEBUG_FILE, "w") as f:
            json.dump(res, f)
            
        return res

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
                
            if input_str:
                try:
                    data = json.loads(input_str)
                except Exception as e_json:
                    try:
                        data = ast.literal_eval(input_str)
                    except Exception as e_ast:
                        err_res = {
                            "error": f"Input parsing failed. JSON error: {str(e_json)}. AST error: {str(e_ast)}",
                            "input_received": input_str
                        }
                        with open(DEBUG_FILE, "w") as f:
                            json.dump(err_res, f)
                        print(json.dumps(err_res))
                        sys.exit(1)
                
                result = train_and_predict(data)
                print(json.dumps(result))
                sys.stdout.flush()
                sys.exit(0)
            else:
                print(json.dumps({"error": "No input provided"}))
                sys.stdout.flush()
                sys.exit(1)
        except Exception as e:
            log_error(e)

except Exception as e:
    log_error(e)
