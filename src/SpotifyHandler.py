import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyHandler:
    def __init__(self):
        # Credentials
        CLIENT_ID = '08ca734d514a4e3b810a8a2220349ef6'
        CLIENT_SECRET = '24e3728d9160403faf10c028a24579ac'
        REDIRECT_URI = 'https://github.com/RileyBagwell/SpotiDrive'  # This is a common local development redirect URI

        # Scope of the authorization
        scope = "user-library-read playlist-read-private playlist-modify-private playlist-modify-public"

        # Initialize the spotify
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                            client_secret=CLIENT_SECRET,
                                                            redirect_uri=REDIRECT_URI,
                                                            scope=scope))

        # Create playlist
        self.playlist_id = ''
        self.create_own_playlist()

        # Get users liked songs
        self.liked_songs = self.sp.current_user_saved_tracks()
        self.get_liked_songs()


    # Create the 'My Next Roadtrip Playlist' playlist
    def create_own_playlist(self):
        playlist_name = 'My Next Roadtrip Playlist (SpotiDrive)'

        # Get user information
        user_info = self.sp.current_user()
        user_id = user_info['id']

        # Check if user has playlist
        playlist_exists = False
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                # Set playlist id to be that existing playlist
                self.playlist_id = playlist['id']

                # Clear the playlist to make room for new songs
                self.clear_playlist()
                playlist_exists = True
                break

        # If the playlist doesn't exist, create the playlist
        if not playlist_exists:
            # Create the playlist
            new_playlist = self.sp.user_playlist_create(user=user_id, name=playlist_name, public=False, collaborative=False)
            self.playlist_id = new_playlist['id']

    # Add songs until the duration of the travel
    def add_songs_until_limit(self, duration):
        # Get length of playlist
        len = self.get_total_playlist_length()

        while len < duration + (duration * 0.05):
            self.add_singular_song()
            len = self.get_total_playlist_length()

    def add_singular_song(self):
        # Get custom playlist
        sd_playlist = self.sp.playlist(playlist_id=self.playlist_id)

        # Add random number of tracks to the user's playlist
        picked_tracks = random.sample(self.liked_songs, 1)

        # Extract the track URIs from the sampled tracks
        track_uris = [track['uri'] for track in picked_tracks]

        self.sp.playlist_add_items(playlist_id=self.playlist_id, items=track_uris)

    # Clears the existing playlist
    def clear_playlist(self):
        # Get the playlist items
        playlist_items = self.sp.playlist_items(playlist_id=self.playlist_id)

        # Cet the items URIs
        track_uris = [item['track']['uri'] for item in playlist_items['items']]

        # Clear the playlist
        self.sp.playlist_remove_all_occurrences_of_items(self.playlist_id,
                                                         items=track_uris)

    # Get all the users liked songs, as the api otherwise only gives 20
    def get_liked_songs(self):
        self.liked_songs = []

        # Increment the number of total liked songs
        offset = 0
        while True:
            user_liked_songs = self.sp.current_user_saved_tracks(limit=50, offset=offset)
            self.liked_songs.extend([{
                'name': item['track']['name'],
                'artist': item['track']['artists'][0]['name'],
                'uri': item['track']['uri']
            } for item in user_liked_songs['items']])
            offset += 50  # Increase the offset to get the next page of liked songs
            if len(user_liked_songs['items']) < 50:
                break

    # Determine the playlist length
    def get_total_playlist_length(self):
        # Get the list of track URIs in the playlist
        tracks = self.sp.playlist_items(self.playlist_id)
        track_uris = [item['track']['uri'] for item in tracks['items']]

        # Fetch audio features for the tracks
        audio_features = self.sp.audio_features(track_uris)

        # Calculate the total duration
        total_duration = 0
        for track in audio_features:
            if track is not None and 'duration_ms' in track:
                total_duration += track['duration_ms']

        # Convert duration to seconds
        total_duration = total_duration / 1000
        return total_duration
