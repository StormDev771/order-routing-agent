from __future__ import annotations
import re
from typing import Optional

US_STATE_CODES = {
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
    "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
    "VA","WA","WV","WI","WY","DC"
}

def normalize_text(s: Optional[str]) -> str:
    if s is None:
        return ""
    return re.sub(r"\s+", " ", s).strip()

def detect_malformed_state(address: str) -> bool:
    # naive parse: try to capture state code as two letters before ZIP
    # e.g. "... , NY 18074"
    if not address:
        return False
    m = re.search(r",\s*([A-Za-z]{2})\s+\d{5}(?:-\d{4})?$", address.strip())
    if not m:
        return False
    state = m.group(1).upper()
    return state not in US_STATE_CODES