import logging
from .trove_commands.command_user import CommandUser
from .trove_commands.command_user_playlists import CommandUserPlaylists
from .trove_commands.command_playlists import CommandPlaylists
from .trove_commands.command_tracks import CommandTracks

# ----------------------------- #
# User Profile Data
# Methods: get_user(), set_user(), delete_user()
# ----------------------------- #

class ATUser(object):
    access_token = None
    user_id = None
    # Application Commands
    user_command = None
    user_playlist_command = None
    playlist_command = None
    track_command = None

    def __init__(self, user_id, access_token):
        self.access_token = access_token
        self.user_id = user_id
        
        # ------------------------- #
        # Each item below must happen in the order specified here
        # [future] - control that will specify when these can be executed
        # ------------------------- #

        # ------------------------- #
        # Called from main application
        # - Create instance of user commands
        # - gets user profile from SpotifyAPI
        # - opens connection to mongoDB User collection
    def open_user_commands(self):
        self.user_command = CommandUser(user_id=self.user_id,access_token=self.access_token)
        return

        # ------------------------- #
        # Called from main application
        # - Create instances of the user playlists commands
        # - gets list of every public playlist a user owns
        # - opens connection to mongoDB User Playlist collection
    def open_user_playlist_commands(self):
        self.user_playlist_command = CommandUserPlaylists(user_id=self.user_id,access_token=self.access_token)
        return

        # ------------------------- #
        # Called from main application
        # - Create instance of the playlist commands
        # - Pulls every playlist for the user instance
        # - opens connection to mongoDB Playlist collection
    def open_playlist_commands(self):
        if self.user_playlist_command == None:
            logging.error("User Playlist command has not been instantiated. Can not open playlist command.")
            return
        playlists = self.user_playlist_command.user_playlists['items']
        playlist_ids = [playlist["id"] for playlist in playlists]
        self.playlist_command = CommandPlaylists(playlist_ids=playlist_ids,access_token=self.access_token)
        return
        
    def open_track_commands(self):
        # if self.playlist_command == None:
        #     logging.error("Playlist command has not been instantiated. Can not open command.")
        #     return
        self.track_command = CommandTracks()
        return
        