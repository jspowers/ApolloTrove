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
        # STEPS MUST FLOW IN FOLLOWING ORDER -
        # 1 - Create instances of the user commands
        # 2 - Create instances of the user playlists
        # 3 - Create instance of the playlist commands
        self.user_command = CommandUser(user_id=user_id,access_token=access_token)
        self.user_playlist_command = CommandUserPlaylists(user_id=user_id,access_token=access_token)


        # playlists = self.user_playlist_command.user_playlists['items']
        # playlist_ids = [playlist["id"] for playlist in playlists]
        # """
        # PICK UP HERE TO STORE THE LIST OF USER PLAYLISTS TO MONGO DB
        # """
        self.playlist_command = CommandPlaylists()
        # pl_docs = self.playlist_command.generate_playlist_list(access_token=self.access_token, playlists=playlist_ids)

        

        #WIP playlist_command = CommandPlaylist( ,access_token=access_token)
        #WIP track_command = CommandTrack( ,access_token=access_token)
