import datetime
import pymongo
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
db = pymongo.MongoClient("mongodb://pokebot:pokemon@127.0.0.1:27017/?authSource=admin")
data = db["pokecord"]
votes = data["User Upvotes"]

@app.route("/", methods=["POST", "GET"])
def index():
    return jsonify(dict(request.headers))

@app.route("/webhook", methods=["POST"])
def webserver():
    if request.headers.get("Authorization") == "pokemon":
        user = request.json.get("user")
        bot = request.json.get("bot")
        checkVoted = votes.find_one({"UserID": user})
        if checkVoted is not None:
            votes.update_one({"UserID": user}, {"$set": {"Streaks": checkVoted["Streaks"] + 1, "Total Votes": checkVoted["Total Votes"] + 1, "Current Votes Count": checkVoted["Current Votes Count"] + 1, "Last Voted At": datetime.datetime.utcnow()}})
            return '', 200
        else:
            return '', 500
    else:
        abort(400)

app.run(host='0.0.0.0')
