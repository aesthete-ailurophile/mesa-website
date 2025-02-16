from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS content (page TEXT PRIMARY KEY, text TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = get_db_connection()
    content = conn.execute('SELECT text FROM content WHERE page = "home"').fetchone()
    events = conn.execute('SELECT title, description FROM events ORDER BY date DESC').fetchall()
    conn.close()
    return render_template('index.html', content=content['text'] if content else "Welcome to MESA!", events=events)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Mechism' and password == 'MechismGpck2025':
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials!"
    return render_template('admin.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    conn = get_db_connection()
    content = conn.execute('SELECT text FROM content WHERE page = "home"').fetchone()
    event_list = conn.execute('SELECT * FROM events ORDER BY date DESC').fetchall()
    conn.close()
    return render_template('dashboard.html', content=content['text'] if content else "", events=event_list)

@app.route('/update_home', methods=['POST'])
def update_home():
    new_content = request.form['content']
    conn = get_db_connection()
    conn.execute('INSERT OR REPLACE INTO content (page, text) VALUES ("home", ?)', (new_content,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form['title']
    description = request.form['description']
    conn = get_db_connection()
    conn.execute('INSERT INTO events (title, description, date) VALUES (?, ?, CURRENT_TIMESTAMP)', (title, description))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()  # Ensure the database is created
    app.run(host='0.0.0.0', port=5000)

