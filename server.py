import datetime
import motor.motor_asyncio
from quart import Quart, request, abort, jsonify

app = Quart(__name__)
db = motor.motor_asyncio.AsyncIOMotorClient("mongodb://pokebot:pokemon@51.79.156.110:27017/?authSource=admin")
data = db["pokecord"]
votes = data["User Upvotes"]

@app.route("/", methods=["POST", "GET"])
async def index():
    return jsonify(dict(request.headers))

@app.route("/webhook", methods=["POST"])
async def webserver():
    if request.headers.get("Authorization") == "pokemon":
        user = request.json.get("user")
        bot = request.json.get("bot")
        checkVoted = await votes.find_one({"UserID": user})
        if checkVoted is None:
            await votes.insert_one({"UserID": user, "Streaks": 1, "Total Votes": 1, "Current Votes Count": 1, "Last Voted At": datetime.datetime.utcnow()})
            return "Sucess", 200
        else:
            await votes.update_one({"UserID": user}, {"$set": {"Streaks": checkVoted["Streaks"] + 1, "Total Votes": checkVoted["Total Votes"] + 1, "Current Votes Count": checkVoted["Current Votes Count"] + 1, "Last Voted At": datetime.datetime.utcnow()}})
            return "Success", 200
    else:
        abort(400)

app.run(host='0.0.0.0')
