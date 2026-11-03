from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home', methods=['POST'])
def home():
    name = request.form.get('name')
    return render_template('home.html', name=name)
