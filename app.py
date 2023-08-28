# from lib2to3.pgen2 import token
# from re import I
from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time


app = Flask(__name__)


app.secret_key = "somethingrandom54321"
app.config['SESSION_COOKIE_NAME'] = 'Test Pall Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    # return 'pls work omg'
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    # return 'redirect'
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))


@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external=False))
        
    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_playlists = []
    iteration = 0
    while True:
        items = sp.current_user_playlists(limit=50, offset=iteration * 50)['items']
        iteration += 1
        # all_playlists += items
        all_playlists.append(items)
        if len(items) < 50:
            break
    # return (all_playlists)
    playlist_names = []
    for x in all_playlists:
        for y in x:
            name = y['name']
            playlist_names.append(name) 
    return str(playlist_names)
    # return str(sp.current_user_playlists(limit=50, offset=0)['items'][0]['name'])
    # return str(sp.current_user_saved_tracks(limit=50, offset=0)['items'][0])
    # all_songs = []
    # iteration = 0
    # while True:
    #     items = sp.current_user_saved_tracks(limit=50, offset=iteration * 50)['items']
    #     iteration += 1
    #     all_songs += items
    #     if len(items) < 50:
    #         break
    # return str(len(all_songs))
    # return "Some drake songs or something"
    
def analyze_track_popularity(playlist_data):
    track_popularity = []
    for track in playlist_data['items']:
        track_name = track['track']['name']
        popularity = track['track']['popularity']
        track_popularity.append((track_name, popularity))
    sorted_track_popularity = sorted(track_popularity, key=lambda x: x[1], reverse=True)
    return sorted_track_popularity

def count_artists(playlist_data):
    artist_counts = {}
    for track in playlist_data['items']:
        for artist in track['track']['artists']:
            artist_name = artist['name']
            artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1
    return artist_counts

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
        client_id = "8bfe8077435543dfa9fb5e84255cfaed",
        client_secret = "ebece8f7edfd4bf681d0c55a754fa321",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read playlist-read-private")