import logging
from flask import render_template, request
from flask_login import current_user, login_required
from ..home import home_bp
from apollotrove.blueprints.spotify_api.modules.spotify_oauth.authorization_startup import checkSpotifyRefresh
from apollotrove.models.user_spotify_auth import UserSpotifyAuth
from apollotrove.models.user_connected_accounts import UserConnectedAccounts
from apollotrove.blueprints.spotify_api.modules.spotify_assets.spotify_user_assets import SpotifyUserAssets
from apollotrove.extensions import apollo_db
from apollotrove.utilities.py_utilities import get_value_mask

@home_bp.route('/')
def home_index():
    if current_user.is_authenticated == False:
        return render_template('index.html')
    else:
        return render_template(
            'index.html',
            current_user_authenticated = current_user.is_authenticated,
            user_username = current_user.username
        )

@home_bp.route('/about')
def home_about():
    return render_template('about.html')

@home_bp.route('/profile', methods=['GET','POST'])
@login_required
def home_profile():
    # ----------------------------- #
    # Linking Spotify Profile 
    # ----------------------------- #
    # Try to get token and return default value if nothing exists
    # Check if refresh is necessary
    checkSpotifyRefresh(current_user.username)


    # Check for user's spotify authorization
    spotify_user_token_data = apollo_db.session.execute(
        apollo_db.select(UserSpotifyAuth).filter_by(username = current_user.username)
        ).scalar_one_or_none()
    if spotify_user_token_data: logging.info('SQLite User Authorization found.')
    else: logging.info('No SQLite User Authorization found.')

    # Check User's spotify profile via Spotify API call
    spotify_user_profile = None
    if spotify_user_token_data and spotify_user_token_data.access_token:
        logging.info('Attempting to get spotify account details using access token.')
        spotify_user_profile = SpotifyUserAssets.get_spotify_current_user_private_profile(spotify_user_token_data.access_token)
    if not spotify_user_profile: 
        logging.warning('No spotify user profile found.')
        return render_template(
            'profile.html',
            current_user_authenticated = current_user.is_authenticated,
            name=current_user.first_name,
            access_token=None,
            expires_timestamp = None,
            spotify_user_profile = None
        )

    # link the spotify user ID to the apollo trove user ID
    user_connected_accounts = apollo_db.session.execute(
        apollo_db.select(UserConnectedAccounts).filter_by(username = current_user.username)
    ).scalar_one_or_none()

    # IF user profile is returned AND user spotify connection doesn't exist
    #   OR if user profile is returned AND user's connected accounts exists but withoud spotify ID
    #   THEN write spotify ID to the apollo_db
    if (spotify_user_profile and user_connected_accounts == None) \
        or (
            spotify_user_profile
            and user_connected_accounts 
            and user_connected_accounts.spotify_id == None
            ):
        user_connected_account = UserConnectedAccounts(
            username = current_user.username,
            spotify_id = spotify_user_profile['id']
        )
        apollo_db.session.add(user_connected_account)
        apollo_db.session.commit()

    # ----------------------------- #
    return render_template(
        'profile.html',
        current_user_authenticated = current_user.is_authenticated,
        user_username = current_user.username,
        name=current_user.first_name,
        access_token_mask=get_value_mask(spotify_user_token_data.access_token),
        expires_timestamp = spotify_user_token_data.expires_timestamp,
        spotify_id = spotify_user_profile.get('id'),
        spotify_display_name = spotify_user_profile.get('display_name'),
        spotify_email = spotify_user_profile.get('email'),
        spotify_account_url = spotify_user_profile.get('external_urls').get('spotify'),
        )


