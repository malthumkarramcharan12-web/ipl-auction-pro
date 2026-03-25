from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

teams = ["MI","CSK","RCB","KKR","DC","PBKS","RR","SRH","GT","LSG"]

players = [
    {"name": "Virat Kohli", "base": 50},
    {"name": "MS Dhoni", "base": 30},
    {"name": "Rohit Sharma", "base": 40},
]

current_player = players[0]
current_bid = current_player["base"]

@app.route('/')
def home():
    return render_template("home.html", teams=teams)

@app.route('/auction', methods=["POST"])
def auction():
    name = request.form.get("name")
    team = request.form.get("team")
    return render_template("auction.html", name=name, team=team, player=current_player, bid=current_bid)

@socketio.on('bid')
def handle_bid(data):
    global current_bid
    current_bid += data['amount']
    emit('update_bid', {"bid": current_bid}, broadcast=True)

@socketio.on('next_player')
def next_player():
    global current_player, current_bid
    current_player = random.choice(players)
    current_bid = current_player["base"]
    emit('new_player', current_player, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
