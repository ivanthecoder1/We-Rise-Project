# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_pymongo import PyMongo
from flask import session
import os 


# -- Initialization section --
app = Flask(__name__)


# # name of database
app.config['MONGO_DBNAME'] = 'edu-project'

app.secret_key = os.getenv('SECRET_KEY')
uri = os.getenv('PASSWORD')

# # URI of database
## forgot how to add in password from .env, need help or review 
app.config['MONGO_URI'] = 'mongodb+srv://admin:' + uri + '@cluster0.zcgya.mongodb.net/edu-project?retryWrites=true&w=majority'
mongo = PyMongo(app)

# -- Routes section --
# INDEX
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# PROGRAMMING
# sets up the methods which allow us to pull input from html
@app.route('/programming', methods = ['GET', 'POST'])
def programming():
    if request.method == "GET":
        # link to our specific collection in database
        cs_events = mongo.db.cs_events
        cs_events = cs_events.find({})
        return render_template('programming.html', cs_events = cs_events)
    else:
        # Takes user input from html
        cs_link = request.form['cs_link']
        cs_description = request.form['cs_description']

        # inserts that user's input into our collection 
        cs_events = mongo.db.cs_events
        cs_events.insert({"URL":cs_link, "Description": cs_description, "Recommender": session["username"] })
        cs_events = cs_events.find({})
        return render_template('programming.html', cs_events = cs_events)

# FINANCE
@app.route('/finance', methods = ['GET', 'POST'])
def finance():
    if request.method == "GET":
        finance_events = mongo.db.finance_events
        finance_events = finance_events.find({})
        return render_template('finance.html', finance_events = finance_events)
    else:
        fin_link = request.form['fin_link']
        fin_description = request.form['fin_description']
        # fin_username = request.form['fin_username']

        finance_events = mongo.db.finance_events
        finance_events.insert({"URL":fin_link, "Description": fin_description, "Recommender": session["username"] })
        finance_events = finance_events.find({})
        return render_template('finance.html', finance_events = finance_events)


# MENTAL HEALTH
@app.route('/mental-health', methods = ['GET', 'POST'])
def mental_health():

    if request.method == "GET":
        mental_events = mongo.db.mental_events
        mental_events = mental_events.find({})
        return render_template('mental-health.html', mental_events = mental_events)
    else:
        men_link = request.form['men_link']
        men_description = request.form['men_description']
        
        mental_events = mongo.db.mental_events
        mental_events.insert({"URL":men_link, "Description": men_description, "Recommender": session["username"] })
        mental_events = mental_events.find({})
        return render_template('mental-health.html', mental_events = mental_events)

# REPORT
@app.route('/report', methods = ['GET', 'POST'])
def report():
    if request.method == "GET":
        reported_users = mongo.db.reported_users
        reported_users = reported_users.find({})
        return render_template('report.html', reported_users = reported_users)
    else:
        reported_user = request.form['reported_user']
        reported_subject = request.form['reported_subject']
        reported_explanation = request.form['reported_explanation']
        
        reported_users = mongo.db.reported_users
        reported_users.insert({"User":reported_user, "Subject": reported_subject, "Explanation": reported_explanation})
        reported_users = reported_users.find({})
        report_status = True 
        thank_message = "Thank you for reporting, we will look into the issue, and try our best to delete their user and link"
        return render_template('report.html', reported_users = reported_users, thank_message = thank_message, report_status = report_status)

# SIGN UP
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        users = mongo.db.user #creates a users database in mongoDB
        # stores form data into user dictionary
        user = {
            "username" : request.form['username'],
            "password" : request.form['password']
        }
        # check if the username already exists in the database
        existing_user = users.find_one({'username': user['username']})
        # make condition to check if username already exists in mongo
        if existing_user is None:
            # adds user data into mongo
            users.insert(user)
            # tell the browser session who the user is
            session["username"] = request.form['username']
            return render_template('index.html')
        else:
            error_signup = "This username already exists!"
            return render_template('signup.html', error_signup = error_signup)
            

# LOGOUT
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    # remove session 
    session.clear()
    return render_template("index.html")

# LOGIN
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        users = mongo.db.user #creates a users database in mongoDB
        # stores form data into user dictionary
        user = {
            "username" : request.form['username'],
            "password" : request.form['password']
        }
        # check if the username already exists in the database
        existing_user = users.find_one({'username': user['username']})
        # make condition to check if username already exists in mongo
        if existing_user:
            # check if password matches
            if user['password'] == existing_user['password']:
                session['username'] = user['username']
                return redirect('/')
            else:
                error = "Incorrect password"
                return render_template('login.html', error = error)
            # tell the browser session who the user is
            session["username"] = request.form['username']
            
            return render_template('index.html')
        else:
            return redirect('/login')
