from flask import Flask, request, redirect, session, render_template, url_for
from flask_socketio import SocketIO
import requests
import os
from urllib.parse import urlencode

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = os.urandom(24)

client_id = "ff7e93d10fb44718b8ee986a1c32f14a"
client_secret = "9856d7100ceb4010901db998dbec107c"
redirect_uri = "http://127.0.0.1:5000/callback"
auth_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"

@app.route('/')
def home():
    return render_template('index.html')  # Rendering the index.html template

@app.route('/login_with_spotify')
def login_with_spotify():
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-read-playback-state user-modify-playback-state"
    }
    return redirect(auth_url + "?" + urlencode(params))  # Redirecting to Spotify authorization URL

@app.route("/callback")
def callback():
    code = request.args.get("code")
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        token_data = response.json()

        session["access_token"] = token_data["access_token"]
        session["refresh_token"] = token_data["refresh_token"]

        return redirect(url_for("success"))
    except requests.RequestException as e:
        return "Error occurred: " + str(e)

@app.route("/success")
def success():
    return render_template("success.html")

@socketio.on('play')
def handle_play():
    access_token = session.get("access_token")
    if access_token:
        print('Play button clicked')
    else:
        print('User not authenticated')

@socketio.on('pause')
def handle_pause():
    access_token = session.get("access_token")
    if access_token:
        print('Pause button clicked')
    else:
        print('User not authenticated')

@socketio.on('next_track')
def handle_next_track():
    access_token = session.get("access_token")
    if access_token:
        print('Next Track button clicked')
    else:
        print('User not authenticated')

if __name__ == "__main__":
    socketio.run(app, debug=True)
