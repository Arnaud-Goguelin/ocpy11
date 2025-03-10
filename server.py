import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for

# --------------------------------------------------
#  functions to load data in json files
# --------------------------------------------------


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


# --------------------------------------------------
#  create Flask app
# --------------------------------------------------

app = Flask(__name__)
app.secret_key = "something_special"

# --------------------------------------------------
#  set data in variables
# --------------------------------------------------


competitions = loadCompetitions()
clubs = loadClubs()

# --------------------------------------------------
#  routes
# --------------------------------------------------


@app.route("/")
def index():
    return render_template("index.html", clubs=clubs)


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = next(
        (club for club in clubs if club["email"] == request.form["email"]),
        None,
    )
    # --- correct crash when unknown email is detected ---
    if not club:
        flash("Email not registered.")
        return redirect(url_for("index"))

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    # TODO: refactor => create a function to return foundClub and foundCompetition
    # and create a better error handling to return more precise messages
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)

    competition_date = datetime.datetime.strptime(
        foundCompetition["date"], "%Y-%m-%d %H:%M:%S"
    )

    # --- correct booking in past competition ---
    if competition_date < datetime.datetime.now():
        flash("Too late, competition already started!")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )
    else:
        foundClub['points'] = int(foundClub['points'])
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )



@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    # --- correct overbooking ---
    if placesRequired > int(competition["numberOfPlaces"]):
        flash("Not enough places available!")
    # --- correct booking negative number ---
    elif placesRequired < 0:
        flash("Need a positive integer!")
    # --- correct booking more than 12 places ---
    elif placesRequired > 12:
        flash("Not allow to book more than 12 places.")
    # --- correct bookings greater than club's points ---
    elif placesRequired > int(club["points"]):
        flash("Not enough points available.")
    else:
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        # --- correct points deduction ---
        club["points"] = int(club["points"]) - placesRequired
        flash("Great-booking complete!")

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


# --------------------------------------------------
#  run app using 'python server.py' command
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
