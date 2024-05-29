import os
import logging
from flask import redirect, url_for
from .spotify_oauth_protocols import (getSpotifyAuth, getSpotifyToken, refreshAuth)
from apollotrove.models.user_spotify_auth import UserSpotifyAuth
from apollotrove.extensions import apollo_db
from datetime import datetime, timedelta 
from dotenv import load_dotenv
load_dotenv()


CLIENT_ID = os.getenv('client_id', 'client_id Path Not Found')
CLIENT_SECRET = os.getenv('client_secret', 'client_secret Path Not Found')

PORT="8000"
CALLBACK_URL="http://localhost"

SCOPE = "user-read-email user-read-private"
TOKEN_DATA = []

def getUser():
    return getSpotifyAuth(CLIENT_ID, f"{CALLBACK_URL}:{PORT}/spotify_api/callback", SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getSpotifyToken(code, CLIENT_ID, CLIENT_SECRET, f"{CALLBACK_URL}:{PORT}/spotify_api/callback")
    logging.info(TOKEN_DATA)
    return TOKEN_DATA


def checkSpotifyRefresh(username):
        # If the token has expired, fire the user token refresh process 
    current_user_spotify_auth = apollo_db.session.execute(
        apollo_db.select(UserSpotifyAuth).filter_by(username = username)
        ).scalar_one_or_none()
    if not current_user_spotify_auth:
        logging.warning('User not found in the SQLite Spotify User Auth Table. Redirecting to user profile.')
        return redirect(url_for('home.home_profile'))
    is_expired = datetime.now() >=current_user_spotify_auth.expires_timestamp  
    if is_expired:
        logging.info('User access token expired. Refreshing token and storing to db.')
        logging.info(f'Using refresh tokne {current_user_spotify_auth.refresh_token}')
        refreshToken(current_user_spotify_auth.refresh_token, current_user_spotify_auth.username)
        refreshed_user_spotify_auth = apollo_db.session.execute(
            apollo_db.select(UserSpotifyAuth).filter_by(username = username)
            ).scalar_one_or_none()
        return refreshed_user_spotify_auth
    else:
        return None


def refreshToken(refresh_token, username):

    #Refreshing User Auth
    token_refresh = refreshAuth(refresh_token, CLIENT_ID, CLIENT_SECRET)
    if not token_refresh:
        logging.warning('Could not refresh the user access token')
        # TODO: Error handling here
        pass

    # Storing refreshed auth to SQLite
    current_user_spotify_auth = apollo_db.session.execute(
        apollo_db.select(UserSpotifyAuth).filter_by(username = username)
        ).scalar_one_or_none()
    current_user_spotify_auth.access_token = token_refresh['access_token']
    current_user_spotify_auth.scope = token_refresh['scope']
    current_user_spotify_auth.expires_in = token_refresh['expires_in']
    reresh_expires_timestamp = datetime.now() + timedelta(seconds=token_refresh['expires_in'])
    current_user_spotify_auth.expires_timestamp = reresh_expires_timestamp
    apollo_db.session.commit()
    logging.info("Refreshed Spotify User Auth")
    return 

def getAccessToken():
    return TOKEN_DATA