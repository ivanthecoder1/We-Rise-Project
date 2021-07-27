# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_pymongo import PyMongo
import os 


# -- Initialization section --
app = Flask(__name__)


events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"}
    ]

cs_events = [
        {"URL":'https://www.codecademy.com/', "Description":"Code academy is an excellent website for learning how to code. It provides you with many exercises and challenges on a variety of computer languages", "Name": "Ivan Zhang"}
    ]

finance_events = [
        {"URL":"Second Day of Classes", "Description":"2019-08-21"},
    ]

mental_events = [
    {"URL":"Third Day of Classes", "Description":"2019-08-21"},
]


# # name of database
app.config['MONGO_DBNAME'] = 'edu-project'

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
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')
def add():
    # connect to the database
    cs_events = mongo.db.cs_events

    # insert new data
    cs_events.insert({"URL":"First Day of Classes", "Description":"2019-08-21"})

    # return a message to the user
    return "cs event added"

# where we add user recommendations to our cs resource link
# bug: the resources aren't saved. they disappear if we refresh
@app.route('/programming', methods = ['GET', 'POST'])
def programming():
    if request.method == "GET":
        cs_events = mongo.db.cs_events
        cs_events = cs_events.find({})
        return render_template('programming.html', cs_events = cs_events)
    else:
        cs_link = request.form['cs_link']
        cs_description = request.form['cs_description']
        cs_username = request.form['cs_username']

        cs_events = mongo.db.cs_events
        cs_events.insert({"URL":cs_link, "Description": cs_description, "Name": cs_username})
        cs_events = cs_events.find({})
        return render_template('programming.html', cs_events = cs_events)

@app.route('/finance', methods = ['GET', 'POST'])
def finance():
    if request.method == "GET":
        finance_events = mongo.db.finance_events
        finance_events = finance_events.find({})
        return render_template('finance.html', finance_events = finance_events)
    else:
        fin_link = request.form['fin_link']
        fin_description = request.form['fin_description']
        fin_username = request.form['fin_username']

        finance_events = mongo.db.finance_events
        finance_events.insert({"URL":fin_link, "Description": fin_description, "Name": fin_username})
        finance_events = finance_events.find({})
        return render_template('finance.html', finance_events = finance_events)


@app.route('/mental-health', methods = ['GET', 'POST'])
def mental_health():
    if request.method == "GET":
        mental_events = mongo.db.mental_events
        mental_events = mental_events.find({})
        return render_template('mental-health.html', mental_events = mental_events)
    else:
        men_link = request.form['men_link']
        men_description = request.form['men_description']
        men_username = request.form['men_username']
        mental_events = mongo.db.mental_events
        mental_events.insert({"URL":men_link, "Description": men_description, "Name": men_username})
        mental_events = mental_events.find({})
        return render_template('mental-health.html', mental_events = mental_events)

# @app.route('/user-resources')

# def user_resources():
#     return render_template('user-resources.html', events = events)

