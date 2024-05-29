from apollotrove.extensions import apollo_db as db

class UserSpotifyAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    access_token = db.Column(db.String(256))
    access_token_timestamp = db.Column(db.DateTime)
    expires_in = db.Column(db.Integer)
    expires_timestamp = db.Column(db.DateTime)
    refresh_token = db.Column(db.String(256))
    scope = db.Column(db.String(128))
    token_type = db.Column(db.String(64))
