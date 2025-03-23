AI Playlist Maker 🎵🤖

🎭 Let Your Mood Pick the Music!

Ever wished your playlist could understand how you feel and play the perfect song automatically? Well, that's exactly what AI Playlist Maker does!

This hobby project uses AI-powered facial emotion detection to scan your face via webcam, determine your mood, and play a matching song on Spotify. No more endless scrolling—just let your vibes control the beats! 🎶

🚀 How It Works

Click the "Find a Song That Matches Your Mood" button.

Your webcam will activate and analyze your facial expression.

The AI detects your mood (e.g., Happy, Sad, Angry, Neutral, etc.).

A song fitting your emotion starts playing instantly via Spotify API. 🎧

Enjoy the perfect soundtrack for your current mood! 😎

🛠 Tech Stack & Features

Python + OpenCV → Captures and analyzes facial expressions

Deep Learning (Emotion Recognition Model) → Detects your mood

Spotify API → Plays a song based on the detected mood

CustomTkinter (GUI Framework) → Provides a sleek and modern UI

Threading → Ensures smooth execution without freezing the interface

🔧 Setup & Installation

📌 1. Clone the Repository

 git clone https://github.com/yourusername/ai-playlist-maker.git
 cd ai-playlist-maker

📌 2. Create & Activate a Virtual Environment (Recommended)

# Windows
python -m venv env
env\Scripts\activate

# Mac/Linux
python3 -m venv env
source env/bin/activate

📌 3. Install Dependencies

pip install -r requirements.txt

📌 4. Set Up Your Spotify API Credentials

Create a .env file in the root folder.

Add the following details (replace with your actual credentials):

SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

(IMPORTANT!) Add .env to .gitignore to keep it private.

📌 5. Run the Project

python main.py

🎨 User Interface Preview

🖥️ A dark-themed modern GUI with smooth animations and Spotify integration!


## 🎨 User Interface Preview

![Home Screen](https://github.com/Xannyy01/Python-Projects/blob/main/screenshot1.png?raw=true)
![Mood Detection](https://github.com/Xannyy01/Python-Projects/blob/main/screenshot2.png?raw=true)



🤝 Contributing

This is just a fun project, but if you have ideas for improvements, feel free to fork the repo and open a PR! 🛠️

💡 Why I Built This?

I wanted a cool, personal project that combines AI, music, and automation. Instead of manually picking songs, I thought—why not let AI handle it? This was a fun learning experience, and I hope you enjoy using it! 😊

📢 Connect With Me!

LinkedIn: Your Name

GitHub: yourusername

🎵 "Let the AI be your DJ!" 🎵

