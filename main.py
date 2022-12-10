from flask import Flask, render_template, request, redirect, send_from_directory
from flask_assets import Bundle, Environment
import pymongo
import re, os
import forms
import hashlib
import utils

#rebuild tailwind css
os.system("tailwindcss -i ./static/src/main.css -o ./static/dist/main.css")

app = Flask(__name__)
assets = Environment(app)
app.config["SECRET_KEY"] = "f5b5256b762796652ad1d33f5e4b853316e67a198074a51e"

css = Bundle("src/main.css", output="dist/main.css")
assets.register("css", css)
css.build()

print("Connecting to the MongoDB server...")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database"]
users = db["users"]
print("Done!")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    form = utils.forms.SignupForm()
    if request.method == "POST":
        username = form.username.data
        email = form.email.data
        password = form.password.data

        uuid = utils.users.generate_uuid()
        token = utils.users.generate_token(uuid, password)

        user = users.find_one({"username": username})

        if user:
            return render_template("signup.html", form=form, error="Username already in use")
        else:
            user = {"uuid": uuid, "username": username, "email": email, "token": token}
            users.insert_one(user)
            return render_template("signup.html", form=form, success="Account created successfully.", redirect="/")

    else:
        return render_template("signup.html", form=form)


@app.route("/login", methods = ["GET", "POST"])
def login():
    form = utils.forms.LoginForm()
    if request.method == "POST":
        username = form.username.data
        password = form.password.data

        user = users.find_one({"username": username})
        uuid = utils.users.get("uuid")

        token = utils.users.generate_token(uuid, password)

        user = users.find_one({"username": username, "token": token})

        if user:
            return render_template("login.html", form=form, success="Logged in successfully")
        else:
            return render_template("login.html", form=form, error="Login credentials invalid")

    else:
        return render_template("login.html", form=form)

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/static/<path:path>")
def serveStaticFile(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)