from __future__ import annotations
import pandas as pd
from .utils import normalize_text

PAYMENT_NORMALIZE = {
    "paid":"Paid",
    "pending":"Pending",
    "fraud suspected":"Fraud Suspected",
    "error":"Error",
    "unknown":"Unknown",
    "": "Unknown",
    None: "Unknown"
}

PRIORITY_NORMALIZE = {
    "high":"High",
    "low":"Low",
    "normal":"Normal",
    "": "Normal",
    None: "Normal"
}

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    # Normalize columns presence
    for col in ["OrderID","CustomerName","Address","PaymentStatus","Priority","Notes"]:
        if col not in out.columns:
            out[col] = ""
    # Normalize text
    out["PaymentStatus"] = (
        out["PaymentStatus"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(PAYMENT_NORMALIZE)
        .fillna("Unknown")
    )
    out["Priority"] = (
        out["Priority"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(PRIORITY_NORMALIZE)
        .fillna("Normal")
    )
    out["Notes"] = out["Notes"].astype(str).str.lower().fillna("")
    out["Address"] = out["Address"].astype(str).apply(normalize_text)
    return out