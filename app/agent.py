from __future__ import annotations
from typing import Dict, Tuple
from .classifier import hybrid_classify

class OrderRoutingAgent:
    def __init__(self):
        # place to load models/resources if needed later
        pass

    def process(self, order: Dict) -> Tuple[str, str]:
        """Reads -> decides -> explains."""
        category, explanation = hybrid_classify(order)
        return category, explanation