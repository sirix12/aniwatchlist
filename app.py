from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests

from helpers import login_required
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# import anime database (which includes usernames,hashes and wishlisted animes)
db = SQL("sqlite:///anime.db")
base = "https://api.jikan.moe/v4/anime"


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    if request.method == "POST":
        # checking for wrong inputs
        if not request.form.get("username"):
            return redirect("/login")

        elif not request.form.get("password"):
            return redirect("/login")

        # find user info and checking password
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return redirect("/login")

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # checking for wrong inputs
        if not request.form.get("username"):
            return redirect("/register")
        elif not request.form.get("password"):
            return redirect("/register")
        elif request.form.get("password") != request.form.get("p_confirmation"):
            return redirect("/register")
        elif db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username")):
            return redirect("/register")
        # add username and hashed password to database
        hashed = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username,hash) VALUES (?, ?)",
                   request.form.get("username"), hashed)
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    if request.method == "POST":
        #checking for wrong inputs
        if not request.form.get("new_password"):
            return redirect("/changepassword")
        # changing the hash of old password to hash of new passwprd of user thats logged in
        hashed = generate_password_hash(request.form.get("new_password"))
        db.execute("UPDATE users SET hash=? WHERE id=?", hashed, session["user_id"])

        return redirect("/")
    else:
        return render_template("changepassword.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        if "name" in request.form:
            name = request.form.get("name")
            name = name.replace(" ", "+")
            # get anime names from the name in search
            responce1 = requests.get(base+"?order_by=score&limit=25&sort=desc&sfw=true&q="+name)
            responce = responce1.json()["data"]
            return render_template("index.html", responce=responce)
        else:
            anime_name = request.form.get("anime_name")
            image_url = request.form.get("image_url")
            print(id)
            user_id = session["user_id"]
            if not db.execute("SELECT anime_name FROM list WHERE userid=? AND anime_name=?", user_id, anime_name):
                db.execute("INSERT INTO list (userid,anime_name,image_url) VALUES (?,?,?)",
                           user_id, anime_name, image_url)

            return redirect("/")

    else:
        responce1 = requests.get("https://api.jikan.moe/v4/top/anime")
        responce = responce1.json()["data"]
        return render_template("index.html", responce=responce)


@app.route("/watchlist", methods=["GET", "POST"])
@login_required
def watchlist():
    if request.method == "POST":
        # removes slected watchlisted anime from the database
        remove_anime = request.form.get("anime_name")
        db.execute("DELETE FROM list WHERE userid=? AND anime_name=?",
                   session["user_id"], remove_anime)
        return redirect("/watchlist")

    else:
        watch_list = db.execute("SELECT * FROM list WHERE userid=?", session["user_id"])
        return render_template("watchlist.html", watch_list=watch_list)
