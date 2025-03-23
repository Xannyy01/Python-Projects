import customtkinter as ctk
import threading
from PIL import Image, ImageTk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from emotion_face import detect_emotion
from tkinter import StringVar
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
# ---------------- SPOTIFY AUTH ---------------- #
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-playback-state user-modify-playback-state"
    )
)

devices = sp.devices()
device_id = devices['devices'][0]['id'] if devices and devices['devices'] else None

# ---------------- DARK THEME ---------------- #
COLORS = {
    "background": "#121212",   # Dark gray background
    "frame": "#1E1E1E",        # Slightly lighter gray for frames
    "text": "#FFFFFF",         # White text for contrast
    "button": "#1DB954",       # Spotify Green
    "button_hover": "#1ED760", # Lighter Green
    "highlight": "#00FF88",
    "quote":"#edf2f4"# Neon green for accents
}

# ---------------- GUI SETUP ---------------- #
ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("AI Mood Music Player")
app.geometry("800x600")
app.configure(fg_color=COLORS["background"])

# ---------------- HEADER ---------------- #
header_frame = ctk.CTkFrame(
    app, fg_color=COLORS["frame"], corner_radius=10
)
header_frame.pack(pady=20, padx=20, fill="x")

header_label = ctk.CTkLabel(
    header_frame, text="AI Mood Music Player",
    font=("Arial", 24, "bold"), text_color=COLORS["text"]
)
header_label.pack(pady=10)

# ---------------- MOOD LABELS ---------------- #
mood_label = ctk.CTkLabel(
    app, text="Detected Mood: -",
    font=("Arial", 18, "bold"), text_color=COLORS["quote"]
)
mood_label.pack(pady=5)

comfort_label = ctk.CTkLabel(
    app, text="",  # empty initially
    font=("Arial", 14, "italic"), text_color=COLORS["highlight"]
)
comfort_label.pack(pady=5)

# ---------------- INFO FRAME (Song + Cover) ---------------- #
info_frame = ctk.CTkFrame(
    app, fg_color=COLORS["frame"], corner_radius=10
)
info_frame.pack(pady=10, padx=20, fill="x")

song_label = ctk.CTkLabel(
    info_frame, text="Song: -",
    font=("Arial", 16, "bold"), text_color=COLORS["text"]
)
song_label.pack(pady=(10, 2))

artist_label = ctk.CTkLabel(
    info_frame, text="Artist: -",
    font=("Arial", 14), text_color=COLORS["text"]
)
artist_label.pack(pady=(2, 10))

album_cover_label = ctk.CTkLabel(info_frame, text="")
album_cover_label.pack(pady=5)

# ---------------- SPOTIFY & EMOTION LOGIC ---------------- #
def play_song(uri):
    """Starts playback of a song on the active Spotify device."""
    if device_id:
        sp.start_playback(device_id=device_id, uris=[uri])
    else:
        song_label.configure(text="No active Spotify device!")

def toggle_playback():
    """Play or pause the current Spotify track."""
    try:
        current_playback = sp.current_playback()
        if current_playback and current_playback["is_playing"]:
            sp.pause_playback()
            play_pause_btn.configure(text="▶ Play")
        else:
            sp.start_playback()
            play_pause_btn.configure(text="⏸ Pause")
    except Exception as e:
        song_label.configure(text="Playback error!")
        print(e)

def fetch_song_info(uri):
    """Fetch song details (name, artist, album cover) and update UI."""
    try:
        track_info = sp.track(uri)
        song_name = track_info["name"]
        artist_name = track_info["artists"][0]["name"]
        album_cover_url = track_info["album"]["images"][0]["url"]

        song_label.configure(text=f"Song: {song_name}")
        artist_label.configure(text=f"Artist: {artist_name}")

        response = requests.get(album_cover_url, stream=True)
        if response.status_code == 200:
            img_data = Image.open(response.raw).resize((150, 150), Image.LANCZOS)
            album_img = ImageTk.PhotoImage(img_data)
            album_cover_label.configure(image=album_img, text="")
            album_cover_label.image = album_img
        else:
            album_cover_label.configure(text="Album cover not found.")
    except Exception as e:
        song_label.configure(text="Error fetching song details")
        print(e)

def play_song_based_on_emotion(emotion):
    """Plays a Spotify track based on the detected emotion and shows comfort message if needed."""
    if not device_id:
        song_label.configure(text="No active Spotify device!")
        return

    mood_music = {
        "happy": "spotify:track:45ZvGm4spSjkkCuuIIDWmx",
        "sad": "spotify:track:5Rj08S8QZa90oWVNbrk13X",
        "angry": "spotify:track:43CCSgqYmldCbKFExsYGVI",
        "fear": "spotify:track:2wHTMZwkLbpM6LNkUBs2Xt",
        "surprise": "spotify:track:3lQPwCmD918SyoiIkw1zqx",
        "neutral": "spotify:track:4xt9T7bqLoLHuHpdVAJdVd"
    }

    # Mood -> Comfort Message
    comfort_messages = {
        "sad": "It's okay, music heals.",
        "fear": "You're stronger than you think."
    }

    track_uri = mood_music.get(emotion)
    if not track_uri:
        mood_label.configure(text="Unknown Mood")
        return

    # Update mood label
    mood_label.configure(text=f"Detected Mood: {emotion.capitalize()}")

    # Update comfort label if sad or fear, else clear
    comfort_label.configure(text=comfort_messages.get(emotion, ""))

    # Fetch song info and play
    fetch_song_info(track_uri)
    play_song(track_uri)

def handle_mood_based_playback():
    """Detect the emotion and play the corresponding song."""
    # Show 'webcam analyzing...' message
    comfort_label.configure(text="Webcam is analyzing your Mood...")
    # Perform detection in a separate thread to avoid blocking UI
    def run_detection():
        emotion = detect_emotion()
        if emotion:
            play_song_based_on_emotion(emotion)
        else:
            mood_label.configure(text="Could not detect mood!")
            comfort_label.configure(text="")
    threading.Thread(target=run_detection).start()

# ---------------- BUTTONS ---------------- #
play_pause_btn = ctk.CTkButton(
    app, text="▶ Play",
    font=("Arial", 18, "bold"),
    command=toggle_playback,
    fg_color=COLORS["button"],
    hover_color=COLORS["button_hover"],
    text_color=COLORS["text"],
    width=250, height=50,
    corner_radius=10
)
play_pause_btn.pack(pady=10)

mood_btn = ctk.CTkButton(
    app, text="Find a Song That Matches Your Mood",
    font=("Arial", 18, "bold"),
    command=handle_mood_based_playback,
    fg_color=COLORS["button"],
    hover_color=COLORS["button_hover"],
    text_color=COLORS["text"],
    width=300, height=50,
    corner_radius=10
)
mood_btn.pack(pady=10)

# ---------------- RUN APPLICATION ---------------- #
app.mainloop()


