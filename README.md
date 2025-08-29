# Prototype Routing & Order Classification Agent (FastAPI)

A lightweight Python service that:
- Cleans/normalizes incoming order data (CSV or JSON).
- Classifies each order into categories (Priority, Payment Review, Address Fix, Hold Shipment, Normal).
- Wraps logic in an **agent** that returns a decision **and an explanation**.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Try it (once server is running)

- Swagger UI: `http://localhost:8000/docs`
- Health check: `GET /health`
- Classify single order: `POST /classify/order`
- Classify CSV file: `POST /classify/file` (multipart upload)
- Classify JSON list: `POST /classify/json` (array of orders)

## CLI (batch classify)
```bash
python classify_cli.py sample_data/orders.csv out.csv
```

## Project Structure
```text
order-routing-agent/
├── app/
│   ├── main.py            # FastAPI app & routes
│   ├── agent.py           # Agent wrapper (reads -> decides -> explains)
│   ├── classifier.py      # Rule-based classifier (hybrid-ready)
│   ├── preprocess.py      # Cleaning & normalization
│   ├── models.py          # Pydantic schemas
│   └── utils.py           # Helpers (address/state validation, text utils)
├── classify_cli.py        # Command-line batch runner
├── requirements.txt
├── README.md
└── sample_data/
    └── orders.csv
```

## Notes
- The classifier is **rule-first** and easy to extend. A placeholder for ML hooks is included.
- Explanations are deterministic and tied to the rule that fired.
- Addresses are minimally validated (basic state-code anomalies, e.g., 'zO').