from langgraph.graph import StateGraph
from playwright.sync_api import sync_playwright
from Agents.detectors_agents import FormState, detect_next_field
from Agents.classifier_agents import classify_field
from Agents.filler_agents import make_fill_field_node
from Agents.orchestrator_agents import advance_focus


def run_app():
    import time
    from pathlib import Path

    # 1️⃣ Get absolute path to your local HTML file
    current_dir = Path(__file__).parent.absolute()
    form_path = current_dir / "form.html"

    if not form_path.exists():
        raise FileNotFoundError(f"❌ form.html not found at {form_path}")

    form_url = f"file://{form_path}"
    print(f"🌐 Opening local form from: {form_url}")

    with sync_playwright() as p:
        print("🚀 Launching Chromium browser...")
        browser = p.chromium.launch(headless=False, slow_mo=200)
        page = browser.new_page()

        # Disable autoplay or unwanted scroll behaviors
        page.add_init_script(
            """
            window.scrollTo(0,0);
            window.addEventListener('wheel', e => e.stopImmediatePropagation(), { capture: true });
            window.addEventListener('scroll', e => window.scrollTo(0, 0));
            """
        )

        # Load the HTML file
        print("📄 Navigating to form...")
        page.goto(form_url, wait_until="domcontentloaded", timeout=30000)
        page.focus('input[name*="first_name"]')
        page.eval_on_selector(":focus", "el => el.style.border='2px solid red'")
        print("✅ Form loaded and ready!")

        # 2️⃣ Build LangGraph workflow
        graph_builder = StateGraph(FormState)

        # Add nodes
        graph_builder.add_node("detect_field", detect_next_field)
        graph_builder.add_node("classify_field", classify_field)
        graph_builder.add_node("fill_field", make_fill_field_node(page))
        graph_builder.add_node("advance_focus", advance_focus)

        # Define transitions
        graph_builder.add_edge("detect_field", "classify_field")
        graph_builder.add_edge("classify_field", "fill_field")
        graph_builder.add_edge("fill_field", "advance_focus")

        # Define start and finish nodes
        graph_builder.set_entry_point("detect_field")
        graph_builder.set_finish_point("advance_focus")

        app = graph_builder.compile()

        # 3️⃣ Define initial form-filling state
        state = {
            "remaining_fields": [
                "first_name",
                "last_name",
                "email",
                "phone",
                "employment_status",
                "resume",
            ],
            "filled_fields": {},
            "focus_index": 0,
        }

        # 4️⃣ Loop through all fields and fill one by one
        print("🧠 Starting automated form filling...\n")

        while state["focus_index"] < len(state["remaining_fields"]):
            try:
                prev_focus = state["focus_index"]
                state = app.invoke(state)

                # Safety: Prevent infinite loop
                if state["focus_index"] == prev_focus:
                    print("⚠️ Stuck on same field; advancing manually...")
                    state["focus_index"] += 1

                time.sleep(0.5)

            except Exception as e:
                print(f"❌ Error during filling step: {e}")
                state["focus_index"] += 1  # skip problematic field

        print("\n🎉 Done filling all fields!")
        print("🧾 Final Filled Fields:")
        print(state["filled_fields"])

        print("\n⏳ Keeping browser open for 5 seconds...")
        time.sleep(5)
        browser.close()
        print("👋 Browser closed successfully.")


if __name__ == "__main__":
    run_app()
