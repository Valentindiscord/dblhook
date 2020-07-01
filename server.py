import datetime
import pymongo
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
db = pymongo.MongoClient("mongodb://pokebot:pokemon@51.79.156.110:27017/?authSource=admin")
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
        link = "https://discordapp.com/api/webhooks/719224502268985385/lZ6_ZFHhcodT6DA4zoQdtXJqNzi5SjL2wW70TyhhLvQkEBZ2SgrJf8kyXM3vR5o8D9qT"
        print(user)
        check = votes.find_one({"UserID": user})
        if check is None:
            voting_time = datetime.datetime.utcnow()
            voting_time -= datetime.timedelta(hours = 13)
            votes.insert_one({"UserID" : user, "Streak" : 0, "Last Voted At" : voting_time, 'Total Votes' : 0, "Current Votes Count" : 0})
            return '', 200
        else:
            voting_time = datetime.datetime.utcnow()
            voting_time -= datetime.timedelta(hours = 13)
            streaks = check["Streaks"] + 1
            tv = check["Total Votes"] + 1
            cv = check["Current Votes Count"] + 1
            votes.update_one({"UserID": user}, {"$set": {"Streaks": streaks, "Total Votes": tv, "Current Votes Count": cv}})
            return '', 200
    else:
        abort(400)
if __name__ == '__main__':
    app.run(debug=True)
