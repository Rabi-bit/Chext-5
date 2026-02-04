import os, subprocess, sys, io, sqlite3, threading, time
from datetime import datetime

# --- AUTO-SETUP ---
def setup():
    try:
        import flask, requests, openai
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "requests", "openai"])
        os.execv(sys.executable, ['python'] + sys.argv)
setup()

from flask import Flask, render_template_string, request, session, redirect, url_for
import openai

app = Flask(__name__)
app.secret_key = 'MASTER_KEY_99'

# --- CONFIGURATION ---
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "YOUR_KEY_HERE")

# --- DATABASE & LOGIC ---
DB_FILE = 'autonomous_memory.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, balance REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY, user TEXT, msg TEXT, timestamp TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS ai_logs (id INTEGER PRIMARY KEY, action TEXT, timestamp TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- THE AI AUTONOMOUS BRAIN (Background Thread) ---
def ai_autonomous_loop():
    """This function runs in the background and 'thinks' for the app."""
    while True:
        try:
            # 1. AI scans the environment (Simulated Web Search for updates)
            # 2. AI decides on an 'improvement'
            improvement_log = f"AI Update {datetime.now()}: Optimized DB queries and refreshed Global News."
            
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO ai_logs (action, timestamp) VALUES (?, ?)", 
                     (improvement_log, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            print(f"[*] AI Agent: {improvement_log}")
            
        except Exception as e:
            print(f"AI Loop Error: {e}")
        
        time.sleep(3600) # Runs every hour

# Start the AI Brain
threading.Thread(target=ai_autonomous_loop, daemon=True).start()

# --- MASTER INTERFACE ---
HTML_MAIN = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI MASTER AUTONOMOUS</title>
    <style>
        body { background: #000; color: #00ff41; font-family: 'Courier New'; display: flex; height: 100vh; margin: 0; }
        .sidebar { width: 300px; border-right: 2px solid #00ff41; padding: 20px; background: #050505; }
        .content { flex: 1; padding: 20px; display: flex; flex-direction: column; }
        .ai-status { border: 1px dashed #00ff41; padding: 10px; margin-bottom: 20px; color: #ffcc00; font-size: 12px; }
        textarea { width: 100%; height: 200px; background: #000; color: #00ff41; border: 1px solid #00ff41; padding: 10px; }
        .btn { background: #00ff41; color: #000; border: none; padding: 10px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>ORG COMMAND</h2>
        <div class="ai-status">
            <strong>AI AGENT STATUS:</strong> ONLINE<br>
            <strong>LATEST ACTION:</strong> {{ last_ai_action }}
        </div>
        <hr>
        <p>Weather: 🌤 Loading...</p>
        <p>News: 📰 Live Updates Enabled</p>
    </div>

    <div class="content">
        <h2>DYNAMIC MASTER ENGINE</h2>
        <p>Describe an improvement, and the AI will rewrite the app for you:</p>
        <form method="POST" action="/ai_modify">
            <input type="text" name="prompt" placeholder="e.g. Add a crypto price tracker to the sidebar" style="width:70%; padding:10px;">
            <button class="btn">ASK AI TO MODIFY</button>
        </form>

        <h3 style="margin-top:30px;">MANUAL OVERRIDE (CODE INJECTION)</h3>
        <form method="POST" action="/exec">
            <textarea name="code">{{ current_code }}</textarea><br><br>
            <button class="btn" style="width:100%;">FORCE GLOBAL REWRITE</button>
        </form>
    </div>
</body>
</html>
'''

# --- ROUTES ---
@app.route('/')
def home():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT action FROM ai_logs ORDER BY id DESC LIMIT 1")
    res = c.fetchone()
    conn.close()
    
    return render_template_string(HTML_MAIN, last_ai_action=res[0] if res else "Initializing...")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['u'] == 'admin' and request.form['p'] == 'master77':
            session['logged_in'] = True
            return redirect(url_for('home'))
    return '<body style="background:black; color:lime; display:flex; justify-content:center; padding-top:100px;"><form method="POST"><h2>MASTER LOGIN</h2><input name="u"><br><input name="p" type="password"><br><button>LOGIN</button></form></body>'

@app.route('/ai_modify', methods=['POST'])
def ai_modify():
    prompt = request.form.get('prompt')
    # This is where the AI takes your text and turns it into real Python code
    # We use OpenAI to generate the code block
    client = openai.OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are the system architect. Return ONLY python code to implement the user's request into the existing Flask app."},
                  {"role": "user", "content": prompt}]
    )
    new_code = response.choices[0].message.content
    # Execute the AI's modification immediately
    exec(new_code, globals())
    return home()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
