import logging
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from ..spotify_api import spotify_api_bp
from apollotrove.extensions import apollo_db
from apollotrove.blueprints.spotify_api.modules.spotify_user_commands.trove_spotify_user_instance import ATSpotUser
from apollotrove.blueprints.spotify_api.modules.spotify_oauth.authorization_startup import checkSpotifyRefresh
from apollotrove.models.user_spotify_auth import UserSpotifyAuth
from apollotrove.models.user_connected_accounts import UserConnectedAccounts
from apollotrove.utilities.mongoQL.mongo_spotify_user import MDBSpotifyUserCollection
from apollotrove.utilities.mongoQL.mongo_spotify_user_playlist import MDBSpotifyUserPlaylistCollection
from apollotrove.utilities.mongoQL.mongo_spotify_playlist import MDBSpotifyPlaylistCollection
# from apollotrove.utilities.mongoQL.mongo_spotify_track import MDBSpotifyTrackCollection


# --------------------------------------------------------------------------------------------------------- #
#
#   UTILITIES
#
# --------------------------------------------------------------------------------------------------------- #

# ----------------------------------- #
# Get spotify userID from 
# ApolloDB:UserConnectedAccounts
# ----------------------------------- #
def get_user_spotify_id():
    # --------------------------- #
    # Get current users spotify ID
    user_connected_accounts = apollo_db.session.execute(
        apollo_db.select(UserConnectedAccounts).filter_by(username = current_user.username)
    ).scalar_one_or_none()
    # TODO: If a user account isn't found, this needs to be a redirect to 
    # profile page with warning message for no spotify user attached
    if user_connected_accounts == None:
        return 'Error: no user connected accounts stored in SQLite.'
    if user_connected_accounts.spotify_id == None:
        return 'Error: No linked spotify ID in user connected accounts.'
    return user_connected_accounts.spotify_id


# ----------------------------------- #
# Create Spotify API call to 
# refresh all user data.
# Returns to spotify user template
# ----------------------------------- #
@spotify_api_bp.route('/refresh_spotify_data', methods=['POST'])
@login_required
def refresh_spotify_user_data():

    # --------------------------- #
    # Get Spotify User ID
    spotify_user_id = get_user_spotify_id()

    # --------------------------- #
    # Refreshing User Spotify Data
    # check for spotify authentication
    checkSpotifyRefresh(current_user.username)

    # --------------------------- #
    # Check for user's spotify authorization
    spotify_user_token_data = apollo_db.session.execute(
        apollo_db.select(UserSpotifyAuth).filter_by(username = current_user.username)
        ).scalar_one_or_none()
    if spotify_user_token_data: logging.info('SQLite User Authorization found.')
    else: logging.info('No SQLite User Authorization found.')

    # ------------------------------------------------------ #
    # SPOTIFY APOLLO TROVE USER INSTANCE
    # Create AT User Instance
    logging.info('Creating instance of ATSpotUser')
    at_instance = ATSpotUser(user_id=spotify_user_id, access_token=spotify_user_token_data.access_token)

    # --------------------------- #
    # Open command to update USER info in MongoDB
    logging.info('Refreshing AT Trove User Playlist')
    # opening will pull user data automatatically and save it to the User instance
    #TODO: change this so it isn't automatic, bad for memory
    at_instance.open_user_commands()
    # at_instance.user_command.get_user() # THIS CURRENTLY HAPPENS AUTOMATICALLY WHEN INSTANTIATED
    at_instance.user_command.set_user(overwrite=True)
    
    # --------------------------- #
    # Open command to update USER PLAYLIST info in MongoDB
    logging.info('Refreshing AT Trove User Playlist')
    # opening will pull userplaylist data automatically and save it to the UserPlaylist instance
    #TODO: change this so it isn't automatic, bad for memory
    at_instance.open_user_playlist_commands()
    # at_instance.user_playlist_command.get_user_playlists() # THIS CURRENTLY HAPPENS AUTOMATICALLY WHEN INSTANTIATED
    at_instance.user_playlist_command.set_user_playlists(overwrite=True)

    # --------------------------- #
    # Open command to update PLAYLIST info in MongoDB
    logging.info('Refreshing AT Trove User Playlist')
    # opening will pull playlist data automatically and save it to the PlaylistCommand instance 
    #TODO: change this so it isn't automatic, bad for memory
    at_instance.open_playlist_commands()
    # at_instance.user_playlist_command.get_user_playlists() # THIS CURRENTLY HAPPENS AUTOMATICALLY WHEN INSTANTIATED
    at_instance.playlist_command.set_playlist(overwrite=True)

    # --------------------------- #
    # Open command to update TRACK info in MongoDB
    logging.info('Refreshing AT Trove Track Data')
    at_instance.open_track_commands()
    # Check to see if list of tracks are available to reference
    # if the playlist command opened without issues, the playlist data will be stored there
    if at_instance.playlist_command.playlist_data:

        # get set() of track IDs from the stored playlist data
        total_track_list = at_instance.track_command.prepare_playlist_trackids(at_instance.playlist_command.playlist_data)
        
        # Call command to get tracks
        # data saved to the track command instance (track_command.track_data)
        at_instance.track_command.get_spotify_track_assets(total_track_list, access_token=at_instance.access_token)

        # Write track data to MongoDB using data stored in the track command
        at_instance.track_command.set_tracks(documents=at_instance.track_command.track_data, overwrite=True)
    
        
    return redirect(url_for('spotify_api.user_spotify_analysis'))
        
    


# --------------------------------------------------------------------------------------------------------- #
#
#   ROUTES TO RENDER TEMPLATES
#
# --------------------------------------------------------------------------------------------------------- #

# ----------------------------------- #
# SPOTIFY USER SUMMARY PAGE ROUTE:
# 1) Get user data stored in MongoDB
# 2) Render the template for Spotify User Page
# ----------------------------------- #
@spotify_api_bp.route('/spotify_user_analysis', methods=['GET'])
@login_required
def user_spotify_analysis():

    # --------------------------- #
    # Get Spotify User ID
    spotify_user_id = get_user_spotify_id()        

    # --------------------------- #
    # Query MongoDB for transferred Spotify User Data
    # Populate User details
    mongo_spot_user = MDBSpotifyUserCollection(user_id = spotify_user_id)
    user_account = mongo_spot_user.get_db_user_profile()

    # Populate User's Playlist details
    mongo_spot_user_playlists = MDBSpotifyUserPlaylistCollection(user_id = spotify_user_id)
    users_playlists = mongo_spot_user_playlists.get_db_user_playlists()
    
    
    # Populate Playlist details
    # -- Leaving Null until I have use case -- #
    # mongo_spot_playlists = MDBSpotifyPlaylistCollection()

    return render_template(
        'spotify_statistics.html',
        current_user_authenticated = current_user.is_authenticated,
        user_username = current_user.username,
        user_account = user_account,
        user_data_refresh_ts = getattr(user_account, 'get', lambda key: [])('request_ts'),
        user_playlist_refresh_ts = getattr(users_playlists, 'get', lambda key: [])('request_ts'),
        # users_playlists = getattr(users_playlists, 'get', lambda key: [])('items'),
    )

# ----------------------------------- #
# SPOTIFY PLAYLIST SUMMARY PAGE ROUTE:
# 1) Get user data stored in MongoDB
# 2) Render the template for Spotify User Page
# ----------------------------------- #
@spotify_api_bp.route('/spotify_user_playlists', methods=['GET'])
@login_required
def user_spotify_playlists():
    
    # --------------------------- #
    # Get Spotify User ID for Playlist Search
    spotify_user_id = get_user_spotify_id()

    # --------------------------- #
    # Query MongoDB to get list of playlist IDs
    mongo_spot_user_playlists = MDBSpotifyUserPlaylistCollection(user_id = spotify_user_id)
    users_playlists = mongo_spot_user_playlists.get_db_user_playlists()
    print(users_playlists['items'][0])
    playlist_ids = [playlist['id'] for playlist in users_playlists['items']]

    # Build analysis data model for Plotly that 
    #   -   Feed the list of Playlist IDs into this action 
    #   -   Each playlist should have levels of aggregations based on data
    #       points from the track features page:
    #       https://developer.spotify.com/documentation/web-api/reference/get-audio-features

    return render_template(
        'spotify_user_playlists.html',
        users_playlists = users_playlists['items'],
    )

    
