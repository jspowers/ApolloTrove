import logging
from flask import render_template, request
from flask_login import current_user, login_required
from ..home import home_bp
from apollotrove.extensions import apollo_db
from apollotrove.utilities.mongoQL.mongo_spotify_user import MDBSpotifyUserCollection
from apollotrove.models.user_connected_accounts import UserConnectedAccounts
from apollotrove.utilities.mongoQL.mongo_spotify_user_playlist import MDBSpotifyUserPlaylistCollection
# from apollotrove.utilities.mongoQL.mongo_spotify_playlist import MDBSpotifyPlaylistCollection
# from apollotrove.utilities.mongoQL.mongo_spotify_track import MDBSpotifyTrackCollection

@home_bp.route('/spotify_analysis', methods=['GET','POST'])
@login_required
def user_spotify_analysis():
    # Route to populate information that is stored in MongoDB    

    # Get current users spotify ID
    user_connected_accounts = apollo_db.session.execute(
        apollo_db.select(UserConnectedAccounts).filter_by(username = current_user.username)
    ).scalar_one_or_none()
    if user_connected_accounts == None:
        return 'Error: no user connected accounts stored in SQLite.'
    if user_connected_accounts.spotify_id == None:
        return 'Error: No linked spotify ID in user connected accounts.'
    spotify_user_id = user_connected_accounts.spotify_id

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
        users_playlists = users_playlists['items'],
    )