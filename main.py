from flask import Flask, render_template, request, redirect, send_from_directory
from flask_assets import Bundle, Environment
import pymongo
import re

import forms

app = Flask(__name__)
assets = Environment(app)
app.config["SECRET_KEY"] = "f5b5256b762796652ad1d33f5e4b853316e67a198074a51e"

css = Bundle("src/main.css", output="dist/main.css")
assets.register("css", css)
css.build()

print("Connecting to the MongoDB server...")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database"]
users = db["users"] #verify that the database is connected
print("Done!")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    form = forms.SignupForm()
    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        print(username, email, password) 
        
        count = 0
        
        for user in users.find({"username": username}):
            count += 1
        
        if count > 0:
            return 'Username already in use'
        else:
            user = {"username": username, "email": email, "password": password}
            users.insert_one(user)
            return 'Signed up'
            
    else:
        return render_template("signup.html", form=form)
        

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        count = 0
        
        for user in users.find({"username": username, "password": password}):
            count += 1
        
        if count > 0:
            return 'Hello, {}!'.format(username)
        else:
            return 'Invalid'
            
    else:
        return render_template("login.html")

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/static/<path:path>")
def serveStaticFile(path):
    return send_from_directory("static", path)
  
if __name__ == "__main__":
  app.run(host="0.0.0.0")