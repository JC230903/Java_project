from flask import Flask, render_template
# from flask_socketio import SocketIO
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# app = Flask(__name__)
# socketio = SocketIO(app)
from flask import Flask, render_template
from flask_socketio import SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Keep track of the current audio state
audio_state = {
    "playing": False,
    "paused": False,
    "track_info": None,
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play")
def play():
    # For now, let's provide a sample audio URL instead of using Spotify
    audio_state["track_info"] = {"preview_url": "path/to/your/audio.mp3"}
    return render_template("play.html", audio_state=audio_state)

# ... (previous SocketIO events remain the same)

if __name__ == "__main__":
    socketio.run(app, debug=True)