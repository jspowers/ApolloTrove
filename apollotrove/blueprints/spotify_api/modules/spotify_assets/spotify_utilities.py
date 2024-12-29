import requests
import logging

def get_batch_spotify_track_audio_features(access_token: str, tracks: list[dict]) -> None:
    '''
    Use this utiliy to modify the track data in place
    '''
    if len(tracks) == 0: return
    
    # get list of track IDs and prepare batches
    track_ids = [track['id'] for track in tracks]
    batch_size = 100
    batches = []
    start = 0
    end = batch_size
    while start <= len(track_ids):
        batches.append(track_ids[start:end])
        start = end
        end += batch_size
    
    track_features = {}
    for batch_number,request_batch in enumerate(batches):
        
        # check mongoDB for how these record structures are being created/stored

        logging.info(f'Getting track analysis for batch {batch_number+1} / {len(batches)}')
        track_string = ','.join(request_batch)
        token_header = {'Authorization': f'Bearer {access_token}'}
        url_ = f'https://api.spotify.com/v1/audio-features?ids={track_string}'
        r = requests.get(url_, headers = token_header).json()

        for track in r.get('audio_features'):
            id = track.get('id', 'ERROR')
            track.pop(id, None)
            track_features[id] = {'audio_features':track}

    
    for track in tracks:
        feat = track_features[track['id']]
        track.update(feat)

    return 
    

track_field_filters =[
    'album.album_type',
    'album.id',
    'album.name',
    'album.type',
    'album.total_tracks',
    'album.release_date',
    'album.release_date_precision',
    'album.images',
    'id',
    'extermal_ids',
    'explicit',
    'name',
    'popularity',
    'track_number',
    'duration_ms',
    'artists.name',
    'artists.id',
]