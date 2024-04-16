from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# SQLite3 Database
DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, sender_id INTEGER, receiver_id INTEGER, message TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         # Simulate SQL injection vulnerability
#         # DO NOT USE THIS IN A REAL APPLICATION
#         sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
#         conn = sqlite3.connect(DATABASE)
#         c = conn.cursor()
#         c.execute(sql)
#         user = c.fetchone()
#         conn.close()
        
#         if user:
#             session['user_id'] = user[0]
#             flash('Logged in successfully!', 'success')
#             return redirect(url_for('inbox'))
#         else:
#             flash('Incorrect username or password', 'error')
    
#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            flash('Logged in successfully!', 'success')
            return redirect(url_for('inbox'))
        else:
            flash('Incorrect username or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another one.', 'error')
        conn.close()
        
    return render_template('signup.html')

@app.route('/inbox')
def inbox():
    if 'user_id' in session:
        user_id = session['user_id']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM messages WHERE receiver_id=?", (user_id,))
        received_messages = c.fetchall()
        conn.close()
        
        return render_template('inbox.html', messages=received_messages)
    else:
        return redirect(url_for('login'))

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if 'user_id' in session:
        if request.method == 'POST':
            receiver_id = request.form['receiver_id']
            message = request.form['message']
            sender_id = session['user_id']
            
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute("INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)", (sender_id, receiver_id, message))
            conn.commit()
            conn.close()
            
            flash('Message sent successfully!', 'success')
            return redirect(url_for('inbox'))
        
        return render_template('send_message.html')
    else:
        return redirect(url_for('login'))

@app.route('/sent_messages')
def sent_messages():
    if 'user_id' in session:
        user_id = session['user_id']
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM messages WHERE sender_id=?", (user_id,))
        sent_messages = c.fetchall()
        conn.close()
        
        return render_template('sent_messages.html', messages=sent_messages)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
