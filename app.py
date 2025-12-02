import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import time
import json
import os

# ============================================================
# 1. CONFIGURATION & DATABASE
# ============================================================
st.set_page_config(page_title="VentureVision Pro", page_icon="🕵️‍♂️", layout="wide")

# Load key from Streamlit Secrets (Safe for Cloud)
MY_API_KEY = st.secrets["GEMINI_KEY"]
genai.configure(api_key=MY_API_KEY)

USER_DB = "users_db.json"
HISTORY_DB = "history_db.json"

if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f: json.dump({}, f)

if not os.path.exists(HISTORY_DB):
    with open(HISTORY_DB, "w") as f: json.dump({}, f)

# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================
def load_data(file):
    try:
        with open(file, "r") as f: return json.load(f)
    except: return {}

def save_data(file, data):
    with open(file, "w") as f: json.dump(data, f)

def register_user(username, password):
    users = load_data(USER_DB)
    if username in users: return False
    users[username] = password
    save_data(USER_DB, users)
    return True

def login_user(username, password):
    users = load_data(USER_DB)
    if username in users and users[username] == password: return True
    return False

def save_to_history(username, topic, report, logs):
    history = load_data(HISTORY_DB)
    if username not in history: history[username] = []
    # Save Report AND Logs
    history[username].insert(0, {"topic": topic, "report": report, "logs": logs})
    save_data(HISTORY_DB, history)

def get_user_history(username):
    history = load_data(HISTORY_DB)
    return history.get(username, [])

# ============================================================
# 3. AI TOOLS
# ============================================================
def get_model():
    try:
        for m in genai.list_models():
            if '2.5-flash' in m.name: return genai.GenerativeModel(m.name)
            if '1.5-flash' in m.name: return genai.GenerativeModel(m.name)
    except: pass
    return genai.GenerativeModel("models/gemini-2.5-flash")

def search_google(query):
    try:
        # Search 'us-en' for better financial data
        results = DDGS().text(query, max_results=5, region="us-en")
        if not results: return "No results found."
        return "\n".join([f"- {r['title']}: {r['body']}" for r in results])
    except Exception as e:
        return f"Search Error: {e}"

def run_agent_process(topic, status_container):
    model = get_model()
    memory = []
    max_steps = 7
    full_logs = f"### 🧠 Agent Thinking Process for: {topic}\n\n"
    
    with status_container.status("🤖 Agent is working...", expanded=True) as s:
        for step in range(1, max_steps + 1):
            st.write(f"**🔄 Step {step}:** Thinking...")
            
            prompt = f"""
            You are an autonomous Venture Capital Agent.
            Goal: Write a Deal Memo for '{topic}'.
            
            History: {memory}
            
            SEARCH STRATEGY:
            - If "revenue" search gives generic pages, try: 'SEARCH: {topic} revenue yahoo finance'
            - If finding people, try: 'SEARCH: {topic} CEO linkedin'
            - Do not repeat failed searches.
            
            INSTRUCTIONS:
            1. Use simple keywords.
            2. OUTPUT FORMAT:
               - To search: 'SEARCH: <query>'
               - To finish: 'ANSWER: <final_report>'
            
            DECIDE NEXT MOVE.
            """
            
            try:
                response = model.generate_content(prompt).text.strip()
            except:
                time.sleep(2)
                continue

            clean_response = response.replace("*", "").strip()
            
            if clean_response.startswith("SEARCH:"):
                query = clean_response.replace("SEARCH:", "").strip()
                st.write(f"👀 **Action:** Searching for *'{query}'*...")
                
                full_logs += f"**Step {step}:** Decided to search for `{query}`.\n"
                result = search_google(query)
                
                snippet = result[:200] + "..." if len(result) > 200 else result
                full_logs += f"> *Result found:* {snippet}\n\n"
                
                memory.append(f"Step {step}: Searched '{query}'. Result: {result}")
                time.sleep(1)
                
            elif clean_response.startswith("ANSWER:"):
                s.update(label="✅ Mission Accomplished!", state="complete", expanded=False)
                full_logs += f"**Step {step}:** Sufficient data found. Generating report.\n"
                return response.split("ANSWER:")[1].strip(), full_logs
                
            else:
                full_logs += f"**Step {step}:** Thought: {response}\n"
                memory.append(f"Step {step} Error: Follow format.")
        
        s.update(label="⚠️ Steps Exhausted (Using best guess)", state="error")
        full_logs += "**Final Step:** Forced timeout. Generating best guess.\n"
        final_rep = model.generate_content(f"Summarize {topic} based on: {memory}").text
        return final_rep, full_logs

# ============================================================
# 4. THE UI LOGIC
# ============================================================
st.markdown("""<style>.stButton>button {width: 100%; border-radius: 5px;}</style>""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
if "current_report" not in st.session_state:
    st.session_state.current_report = ""
if "current_logs" not in st.session_state:
    st.session_state.current_logs = ""

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
        st.title("🔐 VentureVision Pro")
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            l_user = st.text_input("Username", key="l_user")
            l_pass = st.text_input("Password", type="password", key="l_pass")
            if st.button("Log In", type="primary"):
                if login_user(l_user, l_pass):
                    st.session_state.logged_in = True
                    st.session_state.username = l_user
                    st.rerun()
                else:
                    st.error("Invalid Credentials")
        
        with tab2:
            r_user = st.text_input("New Username", key="r_user")
            r_pass = st.text_input("New Password", type="password", key="r_pass")
            if st.button("Create Account"):
                if register_user(r_user, r_pass):
                    st.success("Success! Please Log In.")
                else:
                    st.error("User already exists.")

# --- MAIN DASHBOARD ---
else:
    with st.sidebar:
        st.write(f"👤 **{st.session_state.username}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.markdown("### 🕒 Recent Searches")
        history = get_user_history(st.session_state.username)
        
        # 🛑 FIX: We use 'enumerate' to make every button key unique (apple_0, apple_1)
        for i, item in enumerate(history):
            unique_key = f"{item['topic']}_{i}"
            if st.button(f"📄 {item['topic']}", key=unique_key):
                st.session_state.current_report = item['report']
                st.session_state.current_logs = item['logs']

    st.title("🤖 Agentic Investment Analyst")
    st.caption("Powered by Gemini 2.5 Flash • Autonomous Reasoning Engine")

    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("Target Startup:", placeholder="e.g. Swiggy, Cred")
    with col2:
        st.write("")
        st.write("")
        btn = st.button("🚀 Deploy Agent", type="primary")

    if btn and topic:
        status_box = st.empty()
        report, logs = run_agent_process(topic, status_box)
        save_to_history(st.session_state.username, topic, report, logs)
        st.session_state.current_report = report
        st.session_state.current_logs = logs
        st.rerun()

    if st.session_state.current_report:
        st.markdown("---")
        tab_report, tab_logs = st.tabs(["📄 Deal Memo", "🧠 Agent Brain (Logs)"])
        
        with tab_report:
            st.markdown(st.session_state.current_report)
            st.download_button("📥 Download Report", st.session_state.current_report, "Deal_Memo.md")
            
        with tab_logs:
            st.info("This is the raw reasoning trail of the AI Agent.")
            st.markdown(st.session_state.current_logs)
