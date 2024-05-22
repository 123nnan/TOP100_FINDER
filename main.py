import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Your Authentication can be found in Dashboard>AppName>Settings
CLIENTID = "YOUR CLIENTID" # YOUR CLIENT ID
CLIENTSECRET = "YOUR CLIENTSECRET" #YOUR CLIENT SECRET

# Spotify Authentication using spotipy module

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENTID,
        client_secret=CLIENTSECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="YOUR USERNAME"
    )
)
user = sp.current_user()
user_id = user["id"]

# Scraping Top 100 from Billboard website

url_tag = "https://www.billboard.com/charts/hot-100/"
timeline = input("Which year do you want to travel to?\nType the date in this format YYYY-MM-DD: ")
URL = f"{url_tag}{timeline}"

month_id = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

year = timeline.split("-")[0]
month = timeline.split("-")[1]
day = timeline.split("-")[2]
month_parser = int(month) - 1


response = requests.get(url=URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

all_titles = soup.select("li ul li h3")
song_titles = [song.getText().strip() for song in all_titles]

# Searching the spotify songs by title

song_uri = []
for song in song_titles:
    results = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = results["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Create the playlist.
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"Top100 of {month_id[month_parser]} {day}, {year}",
    public=False,
    collaborative=False,
    description=f"This are the Top 100 songs of {month_id[month_parser]}-{day}-{year}.Enjoy"
)

# Adding songs to the playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)
