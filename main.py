import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/", headers=header)
billboard100 = response.text

soup = BeautifulSoup(billboard100, "html.parser")

top100 = []

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri=REDIRECT_URI,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    show_dialog=True,
    cache_path="token.txt",
    username="21vexx5kuiznfosejmfo5fyxq"
    )
)

user_id = sp.current_user()["id"]
track_uris = []
for song in song_names:
    results = sp.search(q=song, type="track", limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        track_uris.append(track_uri)


playlist = sp.user_playlist_create(user=user_id, name=f"Top 100 Billboard of {date}", public=False, description="Top 100 Billboard")

sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)