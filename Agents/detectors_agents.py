# agents/detector_agent.py
from typing import List, Dict, Optional
from typing_extensions import TypedDict

# This is the shared state schema for the graph.
class FormState(TypedDict, total=False):
    current_field: Optional[str]
    current_type: Optional[str]
    remaining_fields: List[str]
    filled_fields: Dict[str, str]
    focus_index: int

def detect_next_field(state: FormState) -> Dict:
    """
    Picks which field we're currently working on based on focus_index.
    Returns partial state updates.
    """
    remaining = state["remaining_fields"]
    idx = state["focus_index"]

    if idx >= len(remaining):
        # no more fields
        print("✅ All fields are filled or none left.")
        return {"current_field": None}

    field = remaining[idx]
    print(f"👁️ Detecting field: {field}")
    return {"current_field": field}
