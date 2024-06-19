from flask import Flask, request, url_for, session, redirect, render_template
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import re
from datetime import timedelta
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = os.getenv("SESSION_COOKIE_NAME")
TOKEN_INFO = "token_info"
app.permanent_session_lifetime = timedelta(minutes=60)  #added so i don't have to keep deleting the .cache file, Set an appropriate session lifetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('userPlaylists', _external=True))

@app.route('/userPlaylists')
def userPlaylists():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external=False))
        
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.me()  # Fetch the user's information
    user_display_name = user_info['display_name']  # Get the user's display name
    user_profile_picture = user_info['images'][0]['url'] if user_info['images'] else None

    all_playlists = []
    sp.user
    iteration = 0
    while True:
        items = sp.current_user_playlists(limit=50, offset=iteration * 50)['items']
        iteration += 1
        all_playlists.extend(items)
        if len(items) < 50:
            break
            
    # Sort playlists by name in alphabetical order
    all_playlists.sort(key=lambda x: x['name'].lower())
    
    playlist_names = [playlist['name'] for playlist in all_playlists]
    
    return render_template('playlists.html', playlist_names=playlist_names, user_display_name=user_display_name, user_profile_picture=user_profile_picture)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze_playlist():
    if request.method == 'POST':
        playlist_url = request.form.get('playlist_url')
        playlist_id = extract_playlist_id(playlist_url)
        if playlist_id:
            # Redirect to playlist detail page with extracted playlist_id
            return redirect(url_for('playlist_detail_url', playlist_url=playlist_url))
        else:
            error_message = "Invalid playlist URL"
            return render_template('analyze_url.html', error_message=error_message)
    return render_template('analyze_url.html')

def extract_playlist_id(playlist_url):
    # Define a regular expression pattern to match playlist URLs
    pattern = r'^https:\/\/open\.spotify\.com\/playlist\/([a-zA-Z0-9]+)'

    # Use the re.match function to find the playlist ID
    match = re.match(pattern, playlist_url)

    if match:
        playlist_id = match.group(1)  # Extract the playlist ID from the matched group
        return playlist_id

    return None  # Return None if no match is found

@app.route('/playlist_url')
def playlist_detail_url():
    playlist_url = request.args.get('playlist_url')
    if not playlist_url:
        return "Invalid playlist URL"

    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        return "Invalid playlist URL"

    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])

    playlist = sp.playlist(playlist_id)  # Fetch playlist details
    cover_image_url = playlist['images'][0]['url']

    playlist_tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
        playlist_tracks.extend(response['items'])
        offset += 100
        if len(response['items']) < 100:
            break

    artist_counts = count_artists(playlist_tracks)
    sorted_track_popularity = analyze_track_popularity(playlist_tracks)
    # Fetch the playlist's external URLs, specifically the Spotify URL
    playlist_external_urls = playlist.get('external_urls', {}).get('spotify', None)
    
    return render_template('playlist_detail.html', playlist_name=playlist['name'], artist_counts=artist_counts, sorted_track_popularity=sorted_track_popularity, cover_image_url=cover_image_url, playlist_external_urls=playlist_external_urls)

@app.route('/playlist/<playlist_name>')
def playlist_detail(playlist_name):
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external=False))
        
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Get the playlist ID using its name
    playlists = []
    offset = 0
    while True:
        response = sp.current_user_playlists(limit=50, offset=offset)
        playlists.extend(response['items'])
        offset += 50
        if len(response['items']) < 50:
            break
            
    playlist_id = None
    for playlist in playlists:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break
    
    if playlist_id is None:
        return "Playlist not found"
    
    # Fetch playlist details to get cover image URL
    playlist = sp.playlist(playlist_id)
    print(playlist)
    cover_image_url = playlist['images'][0]['url']
    
    # Fetch all playlist tracks
    playlist_tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
        playlist_tracks.extend(response['items'])
        offset += 100
        if len(response['items']) < 100:
            break
    # print(playlist_tracks)
    
    # Calculate artist count using the count_artists function
    artist_counts = count_artists(playlist_tracks)
    sorted_track_popularity = analyze_track_popularity(playlist_tracks)
    # Fetch the playlist's external URLs, specifically the Spotify URL
    playlist_external_urls = playlist.get('external_urls', {}).get('spotify', None)
    
    return render_template('playlist_detail.html', playlist_name=playlist['name'], artist_counts=artist_counts, sorted_track_popularity=sorted_track_popularity, cover_image_url=cover_image_url, playlist_external_urls=playlist_external_urls)

def count_artists(playlist_tracks):
    artist_counts = {}
    for track in playlist_tracks:
        for artist in track['track']['artists']:
            artist_name = artist['name']
            artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1
    
    # Sort the artist counts in descending order
    sorted_artist_counts = dict(sorted(artist_counts.items(), key=lambda item: item[1], reverse=True))
    return sorted_artist_counts
 
def analyze_track_popularity(playlist_tracks):
    track_popularity = []
    for track in playlist_tracks:
        track_name = track['track']['name']
        popularity = track['track']['popularity']
        track_popularity.append((track_name, popularity))
    sorted_track_popularity = sorted(track_popularity, key=lambda x: x[1], reverse=True)
    return sorted_track_popularity

def get_token():
    token_info = session.get(TOKEN_INFO, None)  # if the value doesn't exist turn none
    if not token_info:
        raise Exception("exception")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60  # if token expiration time is past 60 seconds then refresh it
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read playlist-read-private")
