import json, time
from playwright.sync_api import Page

with open("resume_data.json") as f:
    RESUME_DATA = json.load(f)

def make_fill_field_node(page: Page):
    def fill_field(state):
        field = state["current_field"]
        ftype = state.get("current_type", "")
        if not field:
            return {}

        value_key = field.replace(" ", "_").lower()
        value = RESUME_DATA.get(value_key, "")
        print(f"✍️ Filling '{field}' ({ftype}) with '{value}'")

        # 🟥 Highlight current focus before typing
        page.eval_on_selector(":focus", "el => el.style.border='2px solid red'")

        if ftype == "text":
            page.keyboard.type(value, delay=50)
            page.keyboard.press("Tab")
            time.sleep(0.3)

        elif ftype == "radio":
            if value.lower() == "employed":
                page.keyboard.press("ArrowRight")
            else:
                page.keyboard.press("ArrowLeft")
            page.keyboard.press("Tab")
            time.sleep(0.3)

        elif ftype == "file":
            selector = 'input[type="file"][name*="resume"]'
            page.eval_on_selector(selector, "el => el.style.display = 'block'")
            page.set_input_files(selector, RESUME_DATA["resume_path"])
            time.sleep(0.5)
            page.keyboard.press("Tab")

        # 🟩 After tabbing, re-highlight the new active field
        try:
            page.eval_on_selector(":focus", "el => el.style.border='3px solid lime'")
        except Exception:
            pass  # focus might be on button or blank area temporarily

        filled = dict(state.get("filled_fields", {}))
        filled[field] = value
        return {"filled_fields": filled}

    return fill_field
