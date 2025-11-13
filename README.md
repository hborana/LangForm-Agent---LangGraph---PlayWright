# LangForm-Agent---LangGraph---PlayWright
An AI-powered form-automation system built using LangGraph and Playwright. It orchestrates agentic workflows to detect, classify, and fill form fields dynamically using a state-driven graph architecture.

📌 Features

🧠 Agentic automation using LangGraph
🌐 Real browser automation via Playwright (Chromium)
🔍 Field detection, classification, and intelligent filling
🔄 Continuous loop until all fields are filled
🧩 Modular Agents: Detect → Classify → Fill → Advance
🧪 Works on any local or hosted HTML form

🏗️ Architecture Flow
                ┌──────────────────────┐
                │   detect_next_field   │
                └────────────┬─────────┘
                             ▼
                ┌──────────────────────┐
                │    classify_field     │
                └────────────┬─────────┘
                             ▼
                ┌──────────────────────┐
                │      fill_field       │  →  Playwright types, clicks, uploads
                └────────────┬─────────┘
                             ▼
                ┌──────────────────────┐
                │    advance_focus      │
                └────────────┬─────────┘
                             │
                             └─────────────── Loop until no fields remain


⚙️ Installation
1️⃣ Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

2️⃣ Install Dependencies
pip install -r requirements.txt

▶️ Run the Application
python main.py
