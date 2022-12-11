from flask import Flask, render_template, request, redirect, send_from_directory, make_response
from flask_assets import Bundle, Environment
from i18naddress import InvalidAddress, normalize_address

import pymongo
import wtforms
import re
import os
import uuid
import hashlib
import random
import inspect
from utils.utils import *

#===== initialize modules =====

#rebuild tailwind css
os.system("tailwindcss -i ./static/src/main.css -o ./static/dist/main.css")

#initialize flask
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
properties = db["listings"]
locations_cache = db["locations_cache"]
listings_cache = db["listings_cache"]

print("Downloading user-agent strings...")
user_agents = utils.scraper.scrape_user_agents()

#===== api endpoints =====

def api_wrapper(args, func, overrides={}):
    try:
        defaults = get_args(func)
        defaults = {**defaults, **overrides}
        kwargs = parse_args(defaults, args)
    except ValueError as e:
        return {"error": repr(e), "status": 400}

    if "user_agent" in kwargs:
        kwargs["user_agent"] = random.choice(user_agents)
    return func(**kwargs)

@app.route("/api/ip/")
def get_ip_info():
    defaults = {
        "ip": request.remote_addr
    }
    return api_wrapper(request.args, utils.scraper.get_ip_info, defaults)

#args: (query, latitude=0, longitude=0, page_size=5)
@app.route("/api/search/")
def search_locations():
    return api_wrapper(request.args, utils.scraper.get_urls)

#args: (path, page=None, purge_cache=0)
@app.route("/api/location/")
def get_location():
    return api_wrapper(request.args, utils.scraper.get_location)

#args: (id, purge_cache=0)
@app.route("/api/listing/")
def get_listing():
    return api_wrapper(request.args, utils.scraper.get_listing)

#===== frontend endpoints =====

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

@app.route("/login", methods = ["GET", "POST"]) #refactor this later?
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
    if not authenticated:
        return redirect("/login", code=303)

    if request.method == "POST":
        state_code = form.state_code.data
        city = form.city.data
        postal = form.postal.data
        address = form.address.data
        price_per_month = form.price.data
        bedrooms = form.bedrooms.data
        bathrooms = form.bathrooms.data
        square_ft = form.square_ft.data
        lot_size = form.lot_size.data
        property_type = form.property_type.data
        pets = form.pets.data

        listing = properties.find_one({"postal": postal, "address": address})

        try:
            address = normalize_address({
                'country_code': 'US',
                'country_area': state_code,
                'city': city,
                'postal_code': str(postal),
                'street_address': address})

        except InvalidAddress as e:
            return render_template("listing.html", form=form, error="Invalid address")

        if listing:
            return render_template("listing.html", form=form, error="Listing for that address already made.")
        else:
            listing = {"address": address, "price_per_month": price_per_month, "bedrooms": bedrooms, "bathrooms": bathrooms, "square_ft": square_ft, "lot_size": lot_size, "property_type": property_type, "pets": pets}
            properties.insert_one(listing)
            return render_template("listing.html", form=form, success="Listing created successfully.", redirect="/")

    return render_template("listing.html", form=form, authenticated=authenticated)

@app.route("/logout")
def logout():
    response = make_response(render_template("logout.html", success="Successfully logged out."))
    response.set_cookie("uuid", "", expires=0)
    response.set_cookie("token", "", expires=0)
    return response

@app.route("/account", methods = ["GET", "POST"])
def account():
    authenticated = utils.users.is_authenticated(request.cookies)
    form = utils.forms.ProfileForm()
    if not authenticated:
        return redirect("/login", code=303)

    if request.method == "POST":
        name = form.full_name.data
        age = form.age.data
        gender = form.gender.data

        uuid = utils.users.check_cookies(request.cookies).uuid

        db.users.update_one({"uuid": uuid},
            {
                "$set":
                    {
                        "name": name,
                        "age": age,
                        "gender": gender
                    }
            },
            True
        )

        return render_template("account.html", form=form, success="Profile Successfully Updated")

    return render_template("account.html", form=form, authenticated=authenticated)

@app.route("/preferences", methods = ["GET", "POST"])
def preferences():
    authenticated = utils.users.is_authenticated(request.cookies)
    form = utils.forms.RoommatePreferences()
    if not authenticated:
        return redirect("/login", code=303)

    if request.method == "POST":
        relationship = form.relationship.data
        time = form.time.data
        space = form.space.data
        conflicts = form.conflicts.data
        studying = form.studying.data
        shy = form.shy.data
        home = form.home.data
        music = form.music.data
        clean = form.clean.data
        temp = form.temp.data

        uuid = utils.users.check_cookies(request.cookies).uuid

        db.users.update_one({"uuid": uuid},
            {
                "$set":
                    {
                        "prefs": [relationship, time, space, conflicts, studying, shy, home, music, clean, temp]
                    }
            },
            True
        )

        return render_template("roommateform.html", form=form)

    return render_template("roommateform.html", form=form, authenticated=authenticated)

@app.route("/")
def homepage():
    authenticated = utils.users.is_authenticated(request.cookies)
    return render_template("index.html", authenticated=authenticated)

@app.route("/static/<path:path>")
def serveStaticFile(path):
    return send_from_directory("static", path)

#===== launch app =====

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)