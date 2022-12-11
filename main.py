from flask import Flask, render_template, request, redirect, send_from_directory, make_response
from flask_assets import Bundle, Environment
import pymongo
import re, os, uuid, hashlib
import utils

#rebuild tailwind css
os.system("tailwindcss -i ./static/src/main.css -o ./static/dist/main.css")

app = Flask(__name__)
assets = Environment(app)
app.config["SECRET_KEY"] = uuid.uuid4().hex

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
            return render_template("signup.html", form=form, error="Username already in use.")
        else:
            user = {"uuid": uuid, "username": username, "email": email, "token": token}
            users.insert_one(user)
            response = make_response(render_template("signup.html", form=form, success="Account created successfully.", redirect="/"))
            response.set_cookie("uuid", user["uuid"])
            response.set_cookie("token", user["token"])
            return response
    else:
        return render_template("signup.html", form=form)


@app.route("/login", methods = ["GET", "POST"])
def login():
    form = utils.forms.LoginForm()
    if request.method == "POST":
        authenicator = form.username.data
        password = form.password.data

        user = users.find_one({"username": authenicator})

        if user:
            uuid = user.get("uuid")
            token = utils.users.generate_token(uuid, password)
            user = users.find_one({"username": authenicator, "token": token})

        else:
            user = users.find_one({"email": authenicator})

            if user:
                uuid = user.get("uuid")
                token = utils.users.generate_token(uuid, password)
                user = users.find_one({"email": authenicator, "token": token})

        if user:
            response = make_response(render_template("login.html", form=form, success="Logged in successfully.", redirect="/"))
            response.set_cookie("uuid", user["uuid"])
            response.set_cookie("token", user["token"])
            return response
        else:
            return render_template("login.html", form=form, error="Login credentials invalid.")

    else:
        return render_template("login.html", form=form)

@app.route("/listings", methods = ["GET", "POST"])
def listings():
    authenticated = utils.users.is_authenticated(request.cookies)
    form = utils.forms.ListingForm()
    return render_template("listing.html", form=form, authenticated=authenticated)

@app.route("/logout")
def logout():
    response = make_response(render_template("logout.html", success="Successfully logged out."))
    response.set_cookie("uuid", "", expires=0)
    response.set_cookie("token", "", expires=0)
    return response

@app.route("/")
def homepage():
    authenticated = utils.users.is_authenticated(request.cookies)
    return render_template("index.html", authenticated=authenticated)

@app.route("/static/<path:path>")
def serveStaticFile(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)