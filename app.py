import os
from dotenv import load_dotenv

from flask import Flask, session, redirect, url_for, request, render_template

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(64)
load_dotenv('spotify.env')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)


def is_token_validated():
    return sp_oauth.validate_token(cache_handler.get_cached_token())


def validate_token():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/')
def login():
    if not is_token_validated():
        return validate_token()
    return redirect(url_for('home'))


@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args.get('code'))
    return redirect(url_for('home'))


@app.route('/home')
def home():
    if not is_token_validated():
        return redirect(url_for('login'))

    links = [
        {'href': 'playlists', 'title': 'Go to Playlists'},
        {'href': '/page2', 'title': 'Go to Page 2'},
        {'href': '/page3', 'title': 'Go to Page 3'}
    ]

    content_items = [
        {'type': 'links', 'data': links}
    ]

    return render_template('index.html',
                           title='Home Page',
                           heading='Home page',
                           description='Select a link:',
                           content_items=content_items)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/playlists')
def playlists():
    if not is_token_validated():
        return redirect(url_for('login'))

    user_playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in user_playlists['items']]
    playlists_items = [f'{name}: <a href="{url}"> Link</a?>' for name, url in playlists_info]

    content_items = [
        {'type': 'links', 'data': [{'href': '/', 'title': 'Home'}]},
        {'type': 'numbered_list', 'data': playlists_items}
    ]

    return render_template('index.html',
                           title='Playlists',
                           heading='Playlists',
                           description='Here are all your playlists:',
                           content_items=content_items
                           )


if __name__ == '__main__':
    app.run(debug=True)
