import logging
from .trove_commands import (
    CommandUser,
    CommandUserPlaylists,
    CommandPlaylists,
    )

# ----------------------------- #
# User Profile Data
# Methods: get_user(), set_user(), delete_user()
# ----------------------------- #

class ATUser(object):
    access_token = None
    user_id = None
    user_command = None
    user_playlist_command = None
    playlist_command = None

    def __init__(self, user_id, access_token,*args, **kwargs):
        super().__init__(*args, **kwargs)
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
        
        
        # """
        # PICK UP HERE TO STORE THE LIST OF USER PLAYLISTS TO MONGO DB
        # """
        # pl_docs = self.playlist_command.generate_playlist_list(access_token=self.access_token, playlists=playlist_ids)

        

        #WIP playlist_command = CommandPlaylist( ,access_token=access_token)
        #WIP track_command = CommandTrack( ,access_token=access_token)
