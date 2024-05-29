import base64, json, requests
import logging 

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
RESPONSE_TYPE = 'code'   
HEADER = 'application/x-www-form-urlencoded'



def getSpotifyAuth(client_id, redirect_uri, scope):
    data = f"{SPOTIFY_URL_AUTH}client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    return data



def getSpotifyToken(code , client_id, client_secret, redirect_uri):
    body = {
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":redirect_uri
    }
    client_creds_b64 = get_client_credentials(client_id=client_id, client_secret=client_secret)
    headers = {"Content-Type" : HEADER, "Authorization" : f"Basic {client_creds_b64}"}
    response = requests.post(SPOTIFY_URL_TOKEN, params=body, headers = headers)
    return response.json()



def refreshAuth(refresh_token, client_id, client_secret):
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : refresh_token
    }
    client_creds_b64 = get_client_credentials(client_id=client_id, client_secret=client_secret)
    headers = {"Content-Type" : HEADER, "Authorization" : f"Basic {client_creds_b64}"}
    post_refresh = requests.post(SPOTIFY_URL_TOKEN, params=body, headers = headers)
    logging.info(post_refresh.text)
    return post_refresh.json()


# -------------------------------------------------#
#               Utilites                           #
# -------------------------------------------------#
def get_client_credentials(client_id, client_secret):
    """
    Return base encoded 64 string
    """
    if client_id == None or client_secret == None:
        raise Exception("Client ID/Secret must be set")
    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    return client_creds_b64.decode()


