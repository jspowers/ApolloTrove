from datetime import datetime, timedelta
from flask import render_template, redirect, request, url_for
from flask_login import current_user
from ..spotify_api import spotify_api_bp
from apollotrove.models.user_connected_accounts import UserConnectedAccounts
from apollotrove.models.user_spotify_auth import UserSpotifyAuth
from apollotrove.blueprints.spotify_api.modules.spotify_oauth.authorization_startup import checkSpotifyRefresh
from ..modules.spotify_user_commands.trove_spotify_user_instance import ATSpotUser
from apollotrove.extensions import apollo_db
import logging

@spotify_api_bp.route('/spotify_data')
def spotify_request_data():

    spotify_credentials = get_user_access_token()
    spotify_user_id = spotify_credentials[0]
    spotify_access_token = spotify_credentials[1]

    at_spotify_user_instance = ATSpotUser(spotify_user_id,spotify_access_token)
    
    at_spotify_user_instance.open_user_playlist_commands()


    # TODO: Only pull name, photo, owner
    spotify_user_playlists = at_spotify_user_instance.user_playlist_command.user_playlists['items']






    return render_template(
        template_name_or_list="spotify_data_request.html",
        spotify_user_id=spotify_user_id,
        spotify_user_playlists = spotify_user_playlists,
        )


# This get set/post is causing a flask error
# @spotify_api_bp.route('/spotify_data', method=['GET', 'POST'])
# def spotify_request_user_data():
#     # 1) Check if data exists in Mongo DB
#     # 2) Pull data from Mongo DB
#     # 3) If data does not exist in Mongo DB, write to MDB
#     pass


# ------------------------- #
# Utility Methods
# 1) get_user_access_token
# ------------------------- #

def get_user_access_token():
    username = current_user.username
    at_user_accounts = apollo_db.session.execute(
        apollo_db.select(UserConnectedAccounts).filter_by(username=username)
    ).scalar_one_or_none()

    at_user_spotify_id = None 
    logging.info('Checking to see if user exists in SQLite DB')
    if not at_user_accounts:
        logging.warning("User's spotify ID not found in the connected accounts table, redirecting back to profile page.")
        redirect(url_for('home.home_profile'))
    elif not at_user_accounts.spotify_id:
        logging.warning("User does not have a current connected spotify account. Redirecting back to home page.")
        redirect(url_for('home.home_profile'))
    else:
        logging.info('Spotify user ID found. Storing AT Spotify User ID.')
        at_user_spotify_id = at_user_accounts.spotify_id

    # Get Spotify Access Token and refresh if token is expired
    user_spotify_auth = apollo_db.session.execute(
        apollo_db.select(UserSpotifyAuth).filter_by(username = username)
    ).scalar_one_or_none()

    at_user_spotify_access_token = None 
    logging.info('Checking to see if user exists in SQLite DB')
    if not user_spotify_auth:
        logging.warning("User's access token not stored, redirecting back to profile page.")
        redirect(url_for('home.home_profile'))
    elif not user_spotify_auth.access_token:
        logging.warning("User does not have a curernt linked access token. Redirecting back to home page.")
        redirect(url_for('home.home_profile'))
    elif datetime.now() >= user_spotify_auth.expires_timestamp:
        logging.info("user has expired access token, refreshing now.")
        refresh_token = checkSpotifyRefresh(username)
        at_user_spotify_access_token = refresh_token.access_token
    else:
        logging.info('Spotify user ID found. Storing AT Spotify User ID.')
        at_user_spotify_access_token = user_spotify_auth.access_token 


    return at_user_spotify_id, at_user_spotify_access_token