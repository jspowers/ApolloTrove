from datetime import datetime, timedelta
from flask import render_template, redirect, request, url_for
from flask_login import current_user
from ..spotify_api import spotify_api_bp
from ..modules.spotify_oauth.authorization_startup import getUser, getUserToken, checkSpotifyRefresh
from apollotrove.models.user_spotify_auth import UserSpotifyAuth
from apollotrove.extensions import apollo_db
import logging


@spotify_api_bp.route('/')
def spotify_auth_home():
    return render_template('spotify_auth.html')

@spotify_api_bp.route('/login')
def spotify_login():
    response  = getUser()
    return redirect(response)
    
@spotify_api_bp.route('/callback')
def spotify_callback():
    token_data = getUserToken(request.args['code'])
    username = current_user.username
    
    # Token Data
    access_token = token_data['access_token']
    access_token_timestamp = datetime.now()
    expires_in = token_data['expires_in']
    expires_timestamp = datetime.now() + timedelta(seconds=token_data['expires_in'])
    refresh_token = token_data['refresh_token']
    scope = token_data['scope']
    token_type = token_data['token_type']

    # Check whether User has active and valid token stored in SQLite
    logging.info(f'Checking user token db for user: ' + username)
    current_user_token = apollo_db.session.execute(
        apollo_db.select(UserSpotifyAuth).filter_by(username = username)
        ).scalar_one_or_none()
    

    # If current user not found in the token store
    if not current_user_token:
        logging.info('No user token found. Adding user token to db.')
        new_user_token = UserSpotifyAuth(
            username = username
            ,access_token = access_token
            ,access_token_timestamp = access_token_timestamp
            ,expires_in = expires_in
            ,expires_timestamp = expires_timestamp
            ,refresh_token = refresh_token
            ,scope = scope 
            ,token_type = token_type

        )
        apollo_db.session.add(new_user_token)
        apollo_db.session.commit() 

    # If the user already exists, check token accuracy and expiration
    if current_user_token:
        logging.info('User found in the db')
        # If the token has not expired, move on
        if token_data['access_token'] != current_user_token.access_token:
            logging.info('Access Token does not match stores. Updating DB .')
            current_user_token.access_token = access_token
            current_user_token.access_token_timestamp = access_token_timestamp
            current_user_token.expires_in = expires_in
            current_user_token.expires_timestamp = expires_timestamp
            current_user_token.refresh_token = refresh_token
            apollo_db.session.commit()
    
    # Check expiration and refresh if necessary
    refreshed_token_data = checkSpotifyRefresh(username)
    token_data_return = refreshed_token_data or token_data

    return redirect(url_for('home.home_profile', token=refreshed_token_data or token_data))
