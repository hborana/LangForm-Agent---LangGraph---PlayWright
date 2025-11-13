# agents/classifier_agent.py

from typing import Dict, Optional
from typing_extensions import TypedDict

class ClassifierState(TypedDict, total=False):
    current_field: Optional[str]
    current_type: Optional[str]

def classify_field(state: ClassifierState) -> Dict:
    field = state["current_field"]
    if field is None:
        return {}

    f_lower = field.lower()

    if "status" in f_lower:
        ftype = "radio"
    elif "resume" in f_lower:
        ftype = "file"
    else:
        ftype = "text"

    print(f"🔎 Classifying '{field}' as '{ftype}'")
    return {"current_type": ftype}
