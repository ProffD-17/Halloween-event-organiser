from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from cs50 import SQL

# configure app
app = Flask(__name__)
db = SQL("sqlite:///mydata.db")

#configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

user_id = 'unknown'  # Global variable to store the user ID

# handle logging in and out
@app.route('/')
def index():
    # send to home page if logged in, otherwise send to login page
    name = session.get('name')
    if name:
        return redirect('/home')
    return redirect('/login')

@app.route('/home')
def home():
    name = session.get('name')
    id = db.execute("SELECT id FROM users WHERE name = ?", name)
    return render_template('home.html', name=name, id=id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # assume were sent here form login form and get name from form
        name = request.form.get('name')
        if name:
            # store name in session
            session['name'] = name
            # store name in database
            email = request.form.get('email')
            password = request.form.get('password')
            db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", name, email, password)
            user_id = db.execute("SELECT id FROM users WHERE name = ? AND email = ? AND password = ?", name, email, password)
            if not user_id:
                return "Error: User not found in database."
            return redirect('/home')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logged_out.html')


# handle creating events
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        # get details from form and add event in database
        event_name = request.form.get('event_name')
        event_type = request.form.get('event_type')
        event_time = request.form.get('event_time')
        event_location = request.form.get('event_location')
        host_id = request.form.get('host_id')
        db.execute("INSERT INTO events (name, type, time, location, host_id) VALUES (?, ?, ?, ?, ?)", event_name, event_type, event_time, event_location, host_id)
        return redirect('/home')
    return render_template('create_event.html', host_id=user_id)
