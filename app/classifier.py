from __future__ import annotations
from typing import Tuple, Dict
import re
from .utils import detect_malformed_state

# Category constants
PRIORITY = "Priority"
PAYMENT_REVIEW = "Payment Review"
ADDRESS_FIX = "Address Fix"
HOLD_SHIPMENT = "Hold Shipment"
NORMAL = "Normal"

def rule_based_classify(order: Dict) -> Tuple[str, str]:
    notes = (order.get("Notes") or "").lower()
    priority = order.get("Priority") or "Normal"
    pay = order.get("PaymentStatus") or "Unknown"
    addr = order.get("Address") or ""

    # 1) Priority
    if priority == "High" or "urgent" in notes:
        return PRIORITY, "Marked High priority or notes contain 'urgent'."

    # 2) Payment Review
    if pay in {"Pending","Fraud Suspected","Error"} or "manual check" in notes:
        return PAYMENT_REVIEW, f"PaymentStatus='{pay}' or manual review requested."

    # 3) Address Fix
    if "wrong zip" in notes or detect_malformed_state(addr):
        return ADDRESS_FIX, "Notes indicate address issue or malformed state code."

    # 4) Hold Shipment
    if re.search(r"\bhold\b", notes):
        return HOLD_SHIPMENT, "Notes request hold on shipment."

    # 5) Default
    return NORMAL, "No issues detected by rules."

def hybrid_classify(order: Dict) -> Tuple[str, str]:
    # Placeholder for ML-enhanced logic. For now, just call rules.
    return rule_based_classify(order)