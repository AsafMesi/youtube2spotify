from flask import Flask, request, redirect, jsonify, session
import secrets
import urllib.parse
import base64
import requests
from datetime import datetime

CLIENT_ID = '0fccbf92d9c14c38ac5d82e065bb2e70'
CLIENT_SECRET = '50f9e09e37354a3f932caa352fe9d94a'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_STRING = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()
STATE = secrets.token_hex(16)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'


@app.route('/')
def index():
    return "Welcome to my Spotify App! <a href='/login'> Login with Spotify</a>"


@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'

    params = {'client_id': CLIENT_ID,
              'response_type': 'code',
              'scope': scope,
              'redirect_uri': REDIRECT_URI,
              'state': STATE,
              'show_dialog': True}

    auth_url = f'{AUTH_URL}?{urllib.parse.urlencode(params)}'

    return redirect(auth_url)


@app.route('/callback')
def callback():
    if STATE != request.args.get('state'):
        return jsonify({'error': 'state_mismatch'})

    if 'error' in request.args:
        return jsonify({'error': request.args['error']})

    if 'code' not in request.args:
        return jsonify({'error': 'code not in requests.args'})

    req_body = {'grant_type': 'authorization_code',
                'code': request.args['code'],
                'redirect_uri': REDIRECT_URI}

    headers = {'Authorization': f'Basic {AUTH_STRING}',
               'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(TOKEN_URL, data=req_body, headers=headers)
    token_info = response.json()

    session['access_token'] = token_info['access_token']
    session['refresh_token'] = token_info['refresh_token']
    session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

    print(session)
    return redirect('/playlists')


@app.route('/playlists')
def playlists():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {'Authorization': f'Bearer {session['access_token']}'}

    response = requests.get(BASE_URL + 'me/playlists', headers=headers)
    return jsonify(response.json())


@app.route('/refresh-token')
def refresh_token():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {'grant_type': 'refresh_token',
                    'refresh_token': session['refresh_token']}
        headers = {'Authorization': f'Basic {AUTH_STRING}',
                   'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(TOKEN_URL, headers=headers, data=req_body)
        new_token_info = response.json()
        session['access_token'] = new_token_info['access_token']
        session['refresh_token'] = new_token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

    return redirect('/playlists')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
