🚀 VentureVision Pro: Autonomous Investment Agent

VentureVision Pro is an agentic AI application designed to automate venture capital due diligence. Built for the Hack Imagine 2025 hackathon, it replaces hours of manual research with an autonomous loop that thinks, searches, and generates professional investment memos in seconds.

🧠 What Makes This "Agentic"?

Unlike a standard chatbot that just answers from training data, VentureVision uses a ReAct (Reason + Act) loop to behave like a human analyst:

Reasoning: It analyzes a target company and determines what data is missing (e.g., "I need revenue figures").

Tool Use: It autonomously uses DuckDuckGo to search the live web.

Self-Correction: If a search fails (e.g., generic results), the agent detects the failure and pivots its strategy (e.g., "Try searching Yahoo Finance instead").

Memory: It maintains a short-term memory of its actions to avoid repeating mistakes.

✨ Key Features

🕵️‍♂️ Autonomous Research: Just type a startup name (e.g., "Swiggy"), and the agent handles the rest.

🛡️ Smart Search: Auto-detects region (us-en/in-en) and context to filter out spam and find financial data.

🔐 Secure Auth: Full login/registration system with persistent user sessions.

💾 History System: Saves every search and report to a JSON database for later review.

📊 Commercial Output: Generates formatted Deal Memos with "Risk Scores" and downloadable Markdown files.

⚡ Optimized for Free Tier: Runs entirely on the free tier of Google Gemini (Auto-detects Flash/Pro models).

🛠️ Tech Stack

Brain: Google Gemini 2.5 Flash / 1.5 Pro (via google-generativeai)

Tools: DuckDuckGo Search (duckduckgo_search)

Frontend: Streamlit (Custom styled UI)

Backend: Python 3.12+

Data Persistence: JSON-based local database

🚀 Quick Start (Run Locally)

Clone the Repository

git clone [https://github.com/your-username/venture-vision.git](https://github.com/your-username/venture-vision.git)
cd venture-vision


Install Dependencies

pip install -r requirements.txt


Configure API Key

Open app.py.

Find the line: MY_API_KEY = "PASTE_YOUR_AIZA_KEY_HERE"

Replace it with your actual Google Gemini API Key.

(For cloud deployment, use Streamlit Secrets).

Run the App

python -m streamlit run app.py


☁️ Deployment (Streamlit Cloud)

To deploy this app commercially:

Upload this repo to GitHub.

Go to Streamlit Community Cloud.

Connect your repo.

Crucial: Add your API Key in the "Secrets" settings of your app:

GEMINI_KEY = "AIzaSyD..."


Update app.py to use st.secrets["GEMINI_KEY"].

🔮 Future Roadmap

[ ] Multi-Agent Swarm: Separate agents for Legal, Market, and Product analysis.

[ ] PDF Analysis: Drag-and-drop Pitch Decks for instant critique.

[ ] Visualizations: Auto-generate stock price charts and growth graphs.

Built with ❤️ for Hack Imagine 2025 at Huddle Global.
