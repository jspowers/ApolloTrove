from apollotrove.extensions import apollo_db as db

class UserConnectedAccounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    spotify_id = db.Column(db.String(128), nullable=True)
    apple_id = db.Column(db.String(128), nullable=True)
    letterboxd_id = db.Column(db.String(128), nullable=True)
    goodreads_id = db.Column(db.String(128), nullable=True)
