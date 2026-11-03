from flask import Flask, render_template, request, session, redirect
from flask_session import session

# configure app
app = Flask(__name__)

#configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
session(app)

@app.route('/')
def index():
    # send to home page if logged in, otherwise send to login page
    name = session.get('name')
    if name:
        return redirect('/home')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get name from form
        name = request.form.get('name')
        if name:
            # store name in session
            session['name'] = name
            return redirect('/home')
    return render_template('login.html')

@app.route('/home')
def home():
    name = session.get('name')
    return render_template('home.html', name=name)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logged_out.html')