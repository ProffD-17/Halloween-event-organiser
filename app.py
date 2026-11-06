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
                return render_template('login.html', error='password', logged_out=True)
            elif (not (email == user[0]['email'])):
                return render_template('login.html', error='email', logged_out=True)
        else:
            # register user
            db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', username, email, password)
            # store usename in session
            session['username'] = username
            user_id = db.execute('SELECT id FROM users WHERE username = ?', session['username'])
            user_id = user_id[0]['id']
            session['user_id'] = user_id
            return render_template('success.html', success='registered')

        # store usename in session
        session['username'] = username
        user_id = db.execute('SELECT id FROM users WHERE username = ?', session['username'])
        user_id = user_id[0]['id']
        session['user_id'] = user_id
        return redirect('/home')
        
    # got here by link
    return render_template('login.html', logged_out=True)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('success.html', success='log out', logged_out=True)


# handle creating events
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    host_id = db.execute('SELECT id FROM users WHERE username = ?', session['username'])
    host_id = host_id[0]['id']
    if request.method == 'POST':
        # get details from form and add event in database
        event_name = request.form.get('event_name')
        event_type = request.form.get('event_type')
        event_time = request.form.get('event_time')
        event_location = request.form.get('event_location')
        db.execute("INSERT INTO events (name, type, time, location, host_id) VALUES (?, ?, ?, ?, ?)", event_name, event_type, event_time, event_location, host_id)
        return render_template('success.html', success='created_event')
    
    return render_template('create_event.html')


@app.route('/view_events')
def view_events():
    events = db.execute('SELECT * FROM events')
    return render_template('show_events.html', events=events)  


@app.route('/guests', methods=['POST'])
def show_guests():
    # get event id from form
    event_id = request.form.get('event_id')

    guests_ids = db.execute('SELECT guest_id FROM guests WHERE event_id = ?', event_id) # list of dicts of guest ids
    print(guests_ids)
    # loop through the list of dicts and turn it into a list of ids
    guests_id_list = []
    for guest_id_dict in guests_ids:
        guests_id_list.append(guest_id_dict['guest_id'])
    print(guests_id_list)
    guest_names = db.execute('SELECT username FROM users WHERE id IN (?)', guests_id_list)

    # change format from list of dicts to list
    guests_names_list = []
    for guest_name in guest_names:
        print(guest_name)
        guests_names_list.append(guest_name['username'])

    print(guests_names_list)

    event_info = db.execute('SELECT * FROM events WHERE id = ?', event_id)
    event_info = event_info[0]
    return render_template('show_guests.html', guests=guests_names_list, event_name=event_info['name'])

@app.route('/attend', methods=['POST'])
def attend():
    event_id = request.form.get('event_id')
    user_id = session['user_id']
    success = db.execute('INSERT INTO guests (event_id, guest_id) VALUES (?, ?)', event_id, user_id)
    if success:
        return render_template('success.html', success='registered')
    return render_template('failure.html', message='Couldnt sign you up.')


# HANDLE PRIVILEGES
CHANGE_ROLE_PASSWORD = 'password' # password needed to change role
@app.route('/privileges', methods=['GET', 'POST'])
def privileges():
    user_id = session['user_id']
    if request.method == 'GET':
        # display role
        role = db.execute('SELECT role FROM users WHERE id = ?', user_id)
        if role:
            role = role[0]['role']
        else:
            # sholdnt ever happen
            role = 'guest'
        return render_template('privileges.html', role=role)
    
    # check if password given right
    password_given = request.form.get('password')
    if password_given != CHANGE_ROLE_PASSWORD:
        return render_template('failure.html', message='Wrong password.')

    requested_role = request.form.get('role')
    success = db.execute('UPDATE users SET role = ? WHERE id = ?', requested_role, user_id)
    if success:
        return render_template('success.html', success='changed_role')
    return render_template('failure.html', message='Couldnt change role.')

# edit events
@app.route('/edit_event', methods=['POST', 'GET'])
def edit_event():
    if request.method == 'GET':
        event_id = request.args.get('event_id')
        event_info = db.execute('SELECT * FROM events WHERE id = ?', event_id)
        if not event_info:
            return render_template('failure.html', message='Invalid event ID.')
        event_info = event_info[0]
        return render_template('edit_event.html', event_info=event_info)

    # check if user has authorisation to complete the action
    # check if user is host
    user_id = session['user_id']
    event_id = request.form.get('event_id')
    host_id = db.execute('SELECT host_id FROM events WHERE id = ?', event_id)
    if not host_id:
        return render_template('failure.html', message='Invalid event.')
    host_id = host_id[0]['host_id']
    if user_id != host_id:
        # check if user has admin
        role = db.execute('SELECT role FROM users WHERE id = ?', user_id)
        if role:
            role = role[0]['role']
        if role != 'admin':
            return render_template('failure.html', message='You dont have the privilege to complete this action.')
    # get info from form and put it in db
    name = request.form.get('name')
    type = request.form.get('type')
    time = request.form.get('time')
    location = request.form.get('location')
    success = db.execute('UPDATE events SET name = ?, type = ?, time = ?, location = ? WHERE id = ?', name, type, time, location, event_id)
    if not success:
        return render_template('failure.html', message='Couldnt change event information.')
    return render_template('success.html', success='event changed')

