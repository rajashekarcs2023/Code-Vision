# backend/fraud_detection.py
import pandas as pd

# Example data for fraud detection
data = {
    'transaction_id': [1, 2, 3, 4],
    'amount': [9839.64, 1864.28, 181.0, 181.0],
    'isFraud': [0, 0, 1, 1],
}

df = pd.DataFrame(data)

def detect_fraud(transaction_id):
    """Detect fraud based on a transaction ID."""
    # Cast transaction_id to integer to ensure proper comparison
    try:
        transaction_id = int(transaction_id)  # Ensure it's an integer
    except ValueError:
        return f"Invalid transaction ID format: {transaction_id}"

    transaction = df[df['transaction_id'] == transaction_id]

    if transaction.empty:
        return f"Transaction ID {transaction_id} not found."
    
    is_fraud = transaction['isFraud'].values[0]
    if is_fraud:
        return f"Transaction {transaction_id} is flagged as potential fraud."
    else:
        return f"Transaction {transaction_id} is NOT flagged as fraud."
