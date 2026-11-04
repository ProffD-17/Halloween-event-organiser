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


# handle logging in and out
@app.route('/')
def index():
    # send to home page if logged in, otherwise send to login page
    username = session.get('username')
    if username:
        return redirect('/home')
    return redirect('/login')

@app.route('/home')
def home():
    username = session.get('username')
    return render_template('home.html', username=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': # got here by form
        # get info from form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # check if user exists in db
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        if user:
            # check password and email
            
            if not (password == user[0]['password']):
                return render_template('login.html', error='password')
            elif (not (email == user[0]['email'])):
                return render_template('login.html', error='email')
        else:
            # register user
            db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', username, email, password)
            return render_template('success.html', success='registered')

        # store usename in session
        session['username'] = username
        return redirect('/home')
        
    # got here by link
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('success.html', success='log out')


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
    host_id = db.execute('SELECT id FROM users WHERE username = ?', session['username'])
    if host_id:
        host_id = host_id[0]['id']
    return render_template('create_event.html', host_id=host_id)


@app.route('/view_events')
def view_events():
    events = db.execute('SELECT * FROM events')
    return render_template('show_events.html', events=events)  


@app.route('/guests', methods=['POST'])
def guests():
    event_id = request.form.get('event_id')
    # TODO: show a list off all the people going

@app.route('/attend', methods=['POST'])
def attend():
    event_id = request.form.get('event_id')
    # TODO: add user to guest list of event

