import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Provide a playlist name
playlist_name = input('Please enter the playlist name: ')

# Load authentication CSV file
auth_csv_file = 'spotify_auth_info.csv' 
auth_df = pd.read_csv(auth_csv_file)

# Extract authentication information from the spotify_auth_info CSV file
client_id = auth_df['Client ID'][0]
client_secret = auth_df['Client Secret'][0]
redirect_uri = auth_df['Redirect URI'][0]
scope = auth_df['Scope'][0]

# Load playlist CSV file
csv_file = 'Spotify_Songs_Test.csv'
df = pd.read_csv(csv_file)

# Extract song titles and artists
songs = df[['Song Title', 'Artist']].values.tolist()

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope
))

# Create a new playlist with the name provided previously
user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user_id, playlist_name)

# Search for tracks based on song titles and artists, and collect their track IDs
track_ids = []
not_found_songs = []  # List to keep track of songs that weren't found

for song in songs:
    query = f"track:{song[0]} artist:{song[1]}"
    result = sp.search(q=query, type='track', limit=1)
    
    if result['tracks']['items']:
        track_ids.append(result['tracks']['items'][0]['id'])
    else:
        # If not found, search by song title only
        query = f"track:{song[0]}"
        result = sp.search(q=query, type='track', limit=1)
        
        if result['tracks']['items']:
            track_ids.append(result['tracks']['items'][0]['id'])
        else:
            not_found_songs.append(f"{song[0]} by {song[1]}")  # Add to not_found_songs if still not found

# Add the collected track IDs to the newly created playlist
sp.user_playlist_add_tracks(user_id, playlist['id'], track_ids)
print(f"Playlist '{playlist_name}' created successfully!")

# Print out the songs that couldn't be found
if not_found_songs:
    print("The following songs couldn't be found on Spotify:")
    for song in not_found_songs:
        print(song)
else:
    print("All songs were found and added to the playlist.")

# Enjoy!
