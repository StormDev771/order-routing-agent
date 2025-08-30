import time
import pandas as pd
from .agent import OrderRoutingAgent
from sklearn.metrics import accuracy_score, f1_score  # <-- Add this line

def evaluate_model(data):
    """
    Accepts either a file path or a DataFrame.
    """
    if isinstance(data, str):
        df = pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        raise ValueError("Input must be a file path or a DataFrame.")

    agent = OrderRoutingAgent()

    start = time.time()
    df["PredictedCategory"], df["Explanation"] = zip(
        *df.apply(lambda row: agent.process(row.to_dict()), axis=1)  # <-- FIXED HERE
    )
    runtime = time.time() - start

    acc = accuracy_score(df["TrueCategory"], df["PredictedCategory"])
    f1 = f1_score(df["TrueCategory"], df["PredictedCategory"], average="macro")

    metrics = {
        "accuracy": round(acc, 4),
        "f1_macro": round(f1, 4),
        "runtime_sec": round(runtime, 2),
    }
    return metrics, df
