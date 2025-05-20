from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import json
import os  # Needed to get PORT from environment

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Required for session use

# Load balance data
with open('balance_data.json') as f:
    data = json.load(f)
    start_date = datetime.strptime(data['start_date'], "%Y-%m-%d")
    initial_balance = data['initial_balance']
    daily_increment = data['daily_increment']

# Hardcoded login credentials
USERNAME = "jacqueline"
PASSWORD = "securepassword"

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['username'] = username  # Store login in session
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password"
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    today = datetime.now()
    days_passed = (today - start_date).days
    current_balance = initial_balance + (days_passed * daily_increment)

    hour = today.hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return render_template("dashboard.html",
                           greeting=greeting,
                           balance="{:,.2f}".format(current_balance))  # Optional: add comma formatting

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # ✅ This is the line that fixes the Render deployment issue
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
