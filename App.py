import os, subprocess, sys, io
from flask import Flask, request, render_template_string

# 1. AUTO-SETUP
def install():
    try: import flask, requests, openai
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "requests", "openai"])
        os.execv(sys.executable, ['python'] + sys.argv)
install()

import requests, openai

app = Flask(__name__)

# CONFIGURATION (Replace with your keys)
OPENAI_KEY = "your_openai_key"
WEATHER_KEY = "your_openweather_key" # Get free from openweathermap.org
NEWS_KEY = "your_newsapi_key"       # Get free from newsapi.org

state = {"users_online": ["Admin_Master", "User_01", "User_02"], "logs": "System Live."}

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Courier New'; background: #000; color: #0f0; padding: 20px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .box { border: 1px solid #0f0; padding: 15px; background: #050505; }
        .live { color: red; font-weight: bold; }
        input, textarea { width: 90%; background: #111; color: #0f0; border: 1px solid #0f0; padding: 5px; }
        button { background: #0f0; color: #000; border: none; padding: 10px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <h1>OWNER COMMAND CONSOLE</h1>
    
    <div class="grid">
        <div class="box">
            <h3><span class="live">●</span> LIVE IN ORG</h3>
            <ul> {% for user in users %} <li>{{ user }} - <button>BILL ADMIN</button></li> {% endfor %} </ul>
        </div>

        <div class="box">
            <h3>LIVE UPDATES</h3>
            <p><strong>Weather:</strong> {{ weather }}</p>
            <p><strong>Top News:</strong> {{ news }}</p>
        </div>
    </div>

    <div class="box" style="margin-top:20px;">
        <h3>AI CODE INJECTOR (MODIFY APP)</h3>
        <form method="POST" action="/modify">
            <textarea name="code" rows="10">{{ current_code }}</textarea><br><br>
            <button type="submit">EXECUTE GLOBAL MODIFICATION</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def dashboard():
    # Fetch Weather (Example: London)
    w_data = "Clear, 22°C" # Default if no key
    if WEATHER_KEY != "your_openweather_key":
        res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={WEATHER_KEY}&units=metric").json()
        w_data = f"{res['weather'][0]['description']}, {res['main']['temp']}°C"

    return render_template_string(HTML, users=state["users_online"], weather=w_data, news="Breaking: AI System Online", current_code="# Write logic here")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
