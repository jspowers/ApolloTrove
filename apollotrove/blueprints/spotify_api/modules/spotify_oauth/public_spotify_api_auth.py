import base64
import requests
import datetime

class PublicSpotifyAPIAuth(object):
    public_access_token = None
    public_access_token_expires = datetime.datetime.now()
    public_access_token_did_expire = True
    token_url = 'https://accounts.spotify.com/api/token'
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        
    def get_client_credentials(self):
        """
        Return base encoded 64 string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("Client ID/Secret must be set")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}",
            "Content-Type":"application/x-www-form-urlencoded"
        }
        
    def get_token_data(self):
        return {"grant_type": "client_credentials"}
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200,299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        public_access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.public_access_token = public_access_token
        self.public_access_token_expires = expires
        self.public_access_token_did_expire = expires < now
        return True