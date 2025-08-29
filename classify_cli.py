from __future__ import annotations
import sys
import pandas as pd
from app.preprocess import preprocess_df
from app.agent import OrderRoutingAgent

def main():
    if len(sys.argv) < 3:
        print("Usage: python classify_cli.py <input.csv|json> <output.csv>")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]
    if inp.lower().endswith(".csv"):
        df = pd.read_csv(inp)
    else:
        df = pd.read_json(inp)
    df = preprocess_df(df)
    agent = OrderRoutingAgent()
    cats, exps = [], []
    for _, row in df.iterrows():
        cat, exp = agent.process(row.to_dict())
        cats.append(cat); exps.append(exp)
    df["Category"] = cats
    df["Explanation"] = exps
    df.to_csv(outp, index=False)
    print(f"Wrote {len(df)} rows to {outp}")

if __name__ == "__main__":
    main()