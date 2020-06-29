import datetime
import motor.motor_asyncio
import flask
from flask import Flask, request, jsonify

app = Flask(__name__)
mongo = motor.motor_asyncio.AsyncIOMotorClient("mongodb://pokebot:pokemon@51.79.156.110:27017/?authSource=admin")
db = mongo["pokecord"]
vote = db["User Upvote"]

@app.route("/")
async def home():
    return "DBL Webhook server!"

@app.route("/webhook", methods=["POST"])
async def whook():
    if request.headers.get("Authorization") == "pokemon":
        user = request.json.get("user")
        bot = request.json.get("bot")
        reType = request.json.get("type")
        weekend = request.json.get("isWeekend")
        res = await vote.find_one({"UserID": user})
        if res is None:
            await vote.insert_one({"UserID": user, "Last Voted At": datetime.datetime.utcnow(), "Streaks": 0})
        else:
            total = res["Streaks"] + 1
            await vote.update_one({"UserID": user}, {"$set": {"Last Voted At": datetime.datetime.utcnow(), "Streaks": total}})
    else:
        return jsonify({"status": "400", "message": "Not authorized"}, 400)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')    