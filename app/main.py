from __future__ import annotations
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- Added import
from typing import List
import io
import pandas as pd
import math
from concurrent.futures import ThreadPoolExecutor

from .preprocess import preprocess_df
from .models import Order, ClassifiedOrder, OrdersResponse, EvaluationResult  # <-- Add this import
from .agent import OrderRoutingAgent
from .eval import evaluate_model
from .classifier import hybrid_classify

app = FastAPI(title="Order Routing Agent", version="0.1.0")

# Allow local frontend during development
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = OrderRoutingAgent()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/classify/order", response_model=ClassifiedOrder)
def classify_order(order: Order):
    # Convert to DataFrame for preprocessing, then back
    df = pd.DataFrame([order.dict()])
    df = preprocess_df(df)
    rec = df.iloc[0].to_dict()
    category, explanation = agent.process(rec)
    rec.update({"Category": category, "Explanation": explanation})
    return rec

@app.post("/classify/json", response_model=OrdersResponse)
def classify_json(orders: List[Order]):
    if not orders:
        return {"results": [], "count": 0}
    df = pd.DataFrame([o.dict() for o in orders])
    df = preprocess_df(df)
    results = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        cat, exp = agent.process(rec)
        rec.update({"Category": cat, "Explanation": exp})
        results.append(rec)
    return {"results": results, "count": len(results)}

def classify_row(row):
    rec = row.to_dict()
    cat, exp = agent.process(rec)
    rec.update({"Category": cat, "Explanation": exp})
    return rec

@app.post("/classify/file", response_model=OrdersResponse)
async def classify_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        # attempt CSV first
        try:
            df = pd.read_csv(io.BytesIO(content))
        except Exception:
            try:
                df = pd.read_json(io.BytesIO(content))
            except Exception:
                raise HTTPException(status_code=400, detail="Unsupported file format; provide CSV or JSON.")
        df = preprocess_df(df)
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(classify_row, [row for _, row in df.iterrows()]))
        return {"results": results, "count": len(results)}
    finally:
        await file.close()

@app.post("/evaluate")
async def evaluate_orders(file: UploadFile = File(...)):
    # expects dataset with TrueCategory column
    df_path = f"/tmp/{file.filename}"
    with open(df_path, "wb") as f:
        f.write(await file.read())

    metrics, predictions = evaluate_model(df_path)
    return {
        "metrics": metrics,
        "sample_predictions": predictions.head(5).to_dict(orient="records")
    }

@app.post("/evaluate/json", response_model=EvaluationResult)
async def evaluate_orders_json(orders: List[dict]):
    """
    Evaluate a list of orders (as dicts) and return metrics and sample predictions.
    """
    if not orders:
        raise HTTPException(status_code=400, detail="No orders provided.")
    df = pd.DataFrame(orders)
    # Map 'Category' to 'TrueCategory' for evaluation
    if "Category" in df.columns:
        df["TrueCategory"] = df["Category"]
    metrics, predictions = evaluate_model(df)
    return {
        "metrics": metrics,
        "sample_predictions": predictions.head(5).to_dict(orient="records")
    }