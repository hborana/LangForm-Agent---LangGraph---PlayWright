# agents/orchestrator_agent.py
from typing import Dict
from typing_extensions import TypedDict

class OrchestratorState(TypedDict, total=False):
    focus_index: int
    remaining_fields: list

def advance_focus(state: OrchestratorState) -> Dict:
    idx = state["focus_index"] + 1
    done = idx >= len(state["remaining_fields"])

    if done:
        print("✅ All fields filled successfully.")
    else:
        print("➡️ Moving focus to next field index:", idx)

    return {"focus_index": idx}
