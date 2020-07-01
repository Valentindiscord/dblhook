import datetime
#import pymongo
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
#db = pymongo.MongoClient("")
#data = db["pokecord"]
#votes = data["User Upvotes"]

@app.route("/", methods=["POST", "GET"])
def index():
    return jsonify(dict(request.headers))

@app.route("/webhook", methods=["POST"])
def webserver():
    if request.headers.get("Authorization") == "pokemon":
        user = request.json.get("user")
        bot = request.json.get("bot")
        print(user)
        return '', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)
