import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import datetime
import requests
import time
from collections import defaultdict
import json
from timezonefinder import TimezoneFinder
from astral import LocationInfo
from astral.sun import sun
import sys
from datetime import datetime, timedelta
import logging
import signal

# Set up Spotify authentication
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:8888/callback'
WEATHER_API_KEY = 'your_weather_api_key'

SCOPE = ' '.join([
    'user-library-modify',
    'user-modify-playback-state',
    'user-read-playback-state', 
    'user-top-read',
    'playlist-modify-public',
    'playlist-modify-private',
    'user-follow-modify',
    'user-read-recently-played',
    'user-read-currently-playing',
    'streaming',
    'app-remote-control',
    'playlist-read-private',
    'playlist-read-collaborative',
    'user-read-email',
    'user-read-private'
])

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# API rate limiting parameters
MAX_TRACKS_PER_REQUEST = 50
MAX_REQUESTS_PER_HOUR = 1000
SLEEP_BETWEEN_REQUESTS = 0.1

# Add configuration variables
class Config:
    MIN_SLEEP_DURATION = 1800    # 30 minutes
    MAX_SLEEP_DURATION = 14400   # 4 hours
    FORCED_SLEEP_START = 4       # 4 AM
    FORCED_SLEEP_END = 6         # 6 AM
    MIN_SESSION_LENGTH = 900  # 15 minutes
    MAX_SESSION_LENGTH = 7200  # 2 hours
    END_DATE = datetime.now() + timedelta(days=7)
    
    # Randomization weights that themselves change randomly
    WEIGHTS = {
        'playlist_creation_chance': 0.4,
        'playlist_deletion_chance': 0.3,
        'track_interaction_chance': 0.6,
        'market_switching_chance': 0.5,
        'genre_switching_chance': 0.4
    }
    
    @classmethod
    def randomize_weights(cls):
        """Randomly adjust all weights periodically"""
        for key in cls.WEIGHTS:
            cls.WEIGHTS[key] = random.random()

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        filename=f'spotify_reset_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def graceful_shutdown(signum, frame):
    """Handle graceful shutdown on SIGINT/SIGTERM"""
    logging.info("Received shutdown signal. Cleaning up...")
    # Optionally clean up playlists or stop playback
    sys.exit(0)

def random_sleep():
    """Generate random sleep duration with some noise"""
    base_sleep = random.randint(
        Config.MIN_SLEEP_DURATION,
        Config.MAX_SLEEP_DURATION
    )
    noise = random.uniform(-300, 300)  # ±5 minutes noise
    return max(1, base_sleep + noise)

def simulate_human_patterns():
    """Simulate human-like usage patterns with random sleeps and forced night rest"""
    current_hour = datetime.now().hour
    
    # Forced sleep between 4 AM and 6 AM
    if Config.FORCED_SLEEP_START <= current_hour < Config.FORCED_SLEEP_END:
        sleep_duration = (Config.FORCED_SLEEP_END - current_hour) * 3600  # Convert hours to seconds
        logging.info(f"Forced night rest period. Sleeping until 6 AM ({sleep_duration/3600} hours)")
        time.sleep(sleep_duration)
        return True
    
    # Random sleep can occur at any other time
    if random.random() < 0.3:  # 30% chance to sleep at any time
        sleep_duration = random.randint(Config.MIN_SLEEP_DURATION, Config.MAX_SLEEP_DURATION)
        logging.info(f"Random rest period for {sleep_duration/3600:.2f} hours")
        time.sleep(sleep_duration)
        return True
    
    return False

def create_session_playlist():
    """Create a unique playlist for this session"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    name = f"Session_{timestamp}_{session_id}"
    try:
        return sp.user_playlist_create(
            sp.current_user()['id'],
            name,
            public=random.choice([True, False])
        )
    except Exception as e:
        logging.error(f"Failed to create session playlist: {e}")
        return None

def get_context_factors():
    """Get environmental and contextual factors"""
    try:
        # Get IP-based location
        ip_response = requests.get('https://ipapi.co/json/')
        location_data = ip_response.json()
        
        # Get weather data
        weather_response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?"
            f"lat={location_data['latitude']}&lon={location_data['longitude']}"
            f"&appid={WEATHER_API_KEY}&units=metric"
        )
        weather_data = weather_response.json()
        
        # Get time-based info
        tf = TimezoneFinder()
        timezone = tf.timezone_at(
            lat=location_data['latitude'], 
            lng=location_data['longitude']
        )
        
        location = LocationInfo(
            latitude=location_data['latitude'],
            longitude=location_data['longitude']
        )
        sun_info = sun(location.observer)
        
        return {
            'location': {
                'city': location_data.get('city'),
                'country': location_data.get('country'),
                'latitude': location_data.get('latitude'),
                'longitude': location_data.get('longitude')
            },
            'weather': {
                'condition': weather_data['weather'][0]['main'],
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity']
            },
            'time': {
                'hour': datetime.datetime.now().hour,
                'is_day': (
                    sun_info['sunrise'].hour <= datetime.datetime.now().hour <= 
                    sun_info['sunset'].hour
                ),
                'is_weekend': datetime.datetime.now().weekday() >= 5
            }
        }
    except Exception as e:
        print(f"Error getting context factors: {e}")
        return None

def get_random_seed_attributes():
    """Generate random seed attributes influenced by context but maintaining randomness"""
    base_attributes = {
        'min_acousticness': random.random(),
        'max_acousticness': random.random(),
        'target_acousticness': random.random(),
        'min_danceability': random.random(),
        'max_danceability': random.random(),
        'target_danceability': random.random(),
        'min_energy': random.random(),
        'max_energy': random.random(),
        'target_energy': random.random(),
        'min_instrumentalness': random.random(),
        'max_instrumentalness': random.random(),
        'target_instrumentalness': random.random(),
        'min_key': random.randint(0, 11),
        'max_key': random.randint(0, 11),
        'min_liveness': random.random(),
        'max_liveness': random.random(),
        'target_liveness': random.random(),
        'min_loudness': random.uniform(-60, 0),
        'max_loudness': random.uniform(-60, 0),
        'min_mode': random.randint(0, 1),
        'max_mode': random.randint(0, 1),
        'min_popularity': random.randint(0, 100),
        'max_popularity': random.randint(0, 100),
        'min_speechiness': random.random(),
        'max_speechiness': random.random(),
        'target_speechiness': random.random(),
        'min_tempo': random.uniform(50, 200),
        'max_tempo': random.uniform(50, 200),
        'target_tempo': random.uniform(50, 200),
        'min_time_signature': random.randint(3, 7),
        'max_time_signature': random.randint(3, 7),
        'min_valence': random.random(),
        'max_valence': random.random(),
        'target_valence': random.random()
    }
    
    context = get_context_factors()
    if context and random.random() < 0.5:  # 50% chance to use context
        # Time of day adjustments - but completely random
        if context['time']['hour'] < 6 or context['time']['hour'] > 22:
            base_attributes.update({
                'target_energy': random.random(),
                'target_tempo': random.uniform(50, 200),
                'target_valence': random.random()
            })
        elif 6 <= context['time']['hour'] < 10:
            base_attributes.update({
                'target_energy': random.random(),
                'target_valence': random.random()
            })
            
        # Weather influences - but random
        if context['weather']['condition'].lower() in ['rain', 'snow', 'thunderstorm']:
            base_attributes.update({
                'target_acousticness': random.random(),
                'target_instrumentalness': random.random()
            })
        elif context['weather']['condition'].lower() in ['clear', 'sunny']:
            base_attributes.update({
                'target_valence': random.random(),
                'target_energy': random.random()
            })
            
        # Weekend vs Weekday - but random
        if context['time']['is_weekend']:
            base_attributes.update({
                'target_danceability': random.random(),
                'min_popularity': random.randint(0, 100)
            })
        
        # Add extra randomization layer
        for key in base_attributes:
            if random.random() < 0.3:  # 30% chance to override any attribute
                if isinstance(base_attributes[key], float):
                    base_attributes[key] = random.random()
                elif isinstance(base_attributes[key], int):
                    base_attributes[key] = random.randint(0, 100)
    
    return base_attributes

def get_all_available_markets():
    """Get all available Spotify markets"""
    try:
        return sp.available_markets()['markets']
    except:
        return ['US', 'GB', 'DE', 'FR', 'JP', 'AU', 'BR', 'ES']  # Fallback markets

def create_diverse_playlists(num_playlists=50):
    """Create multiple playlists with random characteristics"""
    contexts = [
        'Discover', 'Random', 'Mix', 'Blend', 'Fusion', 'Exploration',
        'Morning', 'Afternoon', 'Evening', 'Night', 'Dawn', 'Dusk',
        'Work', 'Focus', 'Energy', 'Chill', 'Party', 'Mood',
        'Tempo', 'Rhythm', 'Beats', 'Vibes', 'Flow', 'Wave'
    ]
    
    # Add context awareness but maintain randomness
    context = get_context_factors()
    if context and random.random() < 0.5:  # 50% chance to use context
        additional_contexts = [
            context['weather']['condition'],
            f"{context['location']['city']}Vibes",
            'Weekend' if context['time']['is_weekend'] else 'Weekday',
            'DayTime' if context['time']['is_day'] else 'NightTime'
        ]
        # Randomly decide whether to use each additional context
        for ctx in additional_contexts:
            if random.random() < 0.5:  # 50% chance for each
                contexts.append(ctx)
    
    # Add completely random string combinations
    random_contexts = [
        ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5)) for _ in range(10)
    ]
    contexts.extend(random_contexts)
    
    playlists = {}
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for i in range(num_playlists):
        name = f"{random.choice(contexts)}_{timestamp}_{i}"
        description = f"Random exploration playlist {i} created at {timestamp}"
        try:
            playlist = sp.user_playlist_create(
                sp.current_user()['id'],
                name,
                public=random.choice([True, False]),
                description=description
            )
            playlists[name] = playlist['id']
            time.sleep(SLEEP_BETWEEN_REQUESTS)
        except:
            continue
    
    return playlists

def get_massive_track_collection():
    """Get a large diverse collection of tracks using multiple methods"""
    tracks = set()
    markets = get_all_available_markets()
    
    # Get tracks from featured playlists
    try:
        featured = sp.featured_playlists(limit=50)
        for playlist in featured['playlists']['items']:
            results = sp.playlist_tracks(playlist['id'], limit=MAX_TRACKS_PER_REQUEST)
            tracks.update(track['track']['id'] for track in results['items'] if track['track'])
            time.sleep(SLEEP_BETWEEN_REQUESTS)
    except:
        pass

    # Get tracks from different markets and genres
    genres = sp.recommendation_genre_seeds()['genres']
    for market in random.sample(markets, min(10, len(markets))):
        for genre in random.sample(genres, min(20, len(genres))):
            try:
                results = sp.search(
                    q=f'genre:"{genre}"',
                    type='track',
                    market=market,
                    limit=MAX_TRACKS_PER_REQUEST
                )
                tracks.update(track['id'] for track in results['tracks']['items'])
                time.sleep(SLEEP_BETWEEN_REQUESTS)
            except:
                continue

    # Get tracks from recommendations with random attributes
    for _ in range(50):
        try:
            seed_tracks = random.sample(list(tracks), min(5, len(tracks))) if tracks else None
            seed_genres = random.sample(genres, 5)
            
            results = sp.recommendations(
                seed_tracks=seed_tracks,
                seed_genres=seed_genres,
                limit=MAX_TRACKS_PER_REQUEST,
                **get_random_seed_attributes()
            )
            tracks.update(track['id'] for track in results['tracks'])
            time.sleep(SLEEP_BETWEEN_REQUESTS)
        except:
            continue

    return list(tracks)

def get_random_user_playlists():
    """Get a collection of random user playlists"""
    try:
        # Get current user's playlists
        results = sp.current_user_playlists(limit=50)
        user_playlists = []
        
        for playlist in results['items']:
            user_playlists.append({
                'id': playlist['id'],
                'name': playlist['name'],
                'tracks': []
            })
            
            # Get tracks from each playlist
            tracks = sp.playlist_tracks(playlist['id'], limit=MAX_TRACKS_PER_REQUEST)
            user_playlists[-1]['tracks'] = [
                track['track']['id'] for track in tracks['items'] 
                if track['track'] and track['track']['id']
            ]
            time.sleep(SLEEP_BETWEEN_REQUESTS)
            
        return user_playlists
    except Exception as e:
        print(f"Error getting user playlists: {e}")
        return []

def randomize_user_behavior(track_id):
    """Perform random interactions with a track"""
    actions = [
        (lambda: sp.current_user_saved_tracks_add([track_id]), 0.7),
        (lambda: sp.current_user_saved_tracks_delete([track_id]), 0.3),
        (lambda: sp.add_to_queue(f'spotify:track:{track_id}'), 0.5),
        (lambda: sp.start_playback(uris=[f'spotify:track:{track_id}']), 0.8),
        (lambda: sp.next_track(), 0.4),
        (lambda: time.sleep(random.randint(5, 180)), 0.9)
    ]
    
    # Add interaction with user playlists
    if random.random() < 0.3:  # 30% chance to interact with user playlists
        user_playlists = get_random_user_playlists()
        if user_playlists:
            playlist = random.choice(user_playlists)
            if playlist['tracks']:
                random_track = random.choice(playlist['tracks'])
                try:
                    sp.start_playback(uris=[f'spotify:track:{random_track}'])
                    time.sleep(random.randint(5, 180))
                except:
                    pass
    
    for action, probability in actions:
        try:
            if random.random() < probability:
                action()
                time.sleep(SLEEP_BETWEEN_REQUESTS)
        except:
            continue

def massive_algorithm_reset():
    """Execute a massive randomization of Spotify's algorithm"""
    print("Starting massive algorithm reset...")
    
    # Create multiple random playlists
    playlists = create_diverse_playlists()
    print(f"Created {len(playlists)} random playlists")
    
    # Get a massive collection of tracks
    all_tracks = get_massive_track_collection()
    print(f"Collected {len(all_tracks)} unique tracks")
    
    # Distribute tracks across playlists and interact with them
    track_chunks = [all_tracks[i:i + MAX_TRACKS_PER_REQUEST] 
                   for i in range(0, len(all_tracks), MAX_TRACKS_PER_REQUEST)]
    
    for playlist_id in playlists.values():
        # Add random chunks of tracks to each playlist
        chunk = random.choice(track_chunks)
        try:
            sp.playlist_add_items(playlist_id, chunk)
            time.sleep(SLEEP_BETWEEN_REQUESTS)
        except:
            continue
    
    # Perform random interactions with tracks
    print("Performing random interactions with tracks...")
    for track_id in random.sample(all_tracks, min(1000, len(all_tracks))):
        randomize_user_behavior(track_id)
    
    # Clean up by removing some playlists randomly
    for playlist_id in playlists.values():
        if random.random() < 0.3:  # 30% chance to remove each playlist
            try:
                sp.current_user_unfollow_playlist(playlist_id)
                time.sleep(SLEEP_BETWEEN_REQUESTS)
            except:
                continue
    
    print("Massive algorithm reset complete!")

def run_continuous_reset():
    """Run the reset process continuously for a week"""
    setup_logging()
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    
    logging.info("Starting week-long algorithm reset...")
    
    while datetime.now() < Config.END_DATE:
        try:
            current_hour = datetime.now().hour
            
            # Check for forced sleep period first
            if Config.FORCED_SLEEP_START <= current_hour < Config.FORCED_SLEEP_END:
                simulate_human_patterns()
                continue
            
            # Randomize all configuration weights
            Config.randomize_weights()
            
            # Check for random sleep
            if simulate_human_patterns():
                continue
                
            # Determine session length
            session_length = random.randint(
                Config.MIN_SESSION_LENGTH,
                Config.MAX_SESSION_LENGTH
            )
            
            # Ensure session doesn't run into forced sleep period
            next_forced_sleep = datetime.now().replace(
                hour=Config.FORCED_SLEEP_START, 
                minute=0, 
                second=0
            )
            if datetime.now().hour >= Config.FORCED_SLEEP_START:
                next_forced_sleep += timedelta(days=1)
                
            time_until_forced_sleep = (next_forced_sleep - datetime.now()).total_seconds()
            session_length = min(session_length, time_until_forced_sleep)
            
            session_end = datetime.now() + timedelta(seconds=session_length)
            
            logging.info(f"Starting new session of {session_length/60:.2f} minutes")
            
            # ... rest of the session code ...

        except Exception as e:
            logging.error(f"Session error: {e}")
            time.sleep(300)  # Sleep 5 minutes on error
            continue

def is_protected_playlist(playlist):
    """Check if playlist should be protected"""
    if not Config.PRESERVE:
        return False  # If PRESERVE is False, no playlists are protected
        
    try:
        # Only check protections if PRESERVE is True
        return (
            playlist['owner']['id'] == Config.USER_ID or  # User owned
            Config.USER_ID in sp.playlist(playlist['id'])['followers'] or  # User is collaborator
            any(  # User saved/followed
                saved['id'] == playlist['id'] 
                for saved in sp.current_user_playlists()['items']
            )
        )
    except:
        return True  # If error, protect playlist only if PRESERVE is True

def get_safe_playlists():
    """Get playlists that are safe to modify"""
    try:
        all_playlists = sp.current_user_playlists()['items']
        if not Config.PRESERVE:
            return all_playlists  # If PRESERVE is False, all playlists are safe
        
        # Only filter if PRESERVE is True
        return [
            playlist for playlist in all_playlists 
            if not is_protected_playlist(playlist)
        ]
    except Exception as e:
        logging.error(f"Error getting safe playlists: {e}")
        return []

def cleanup_playlists():
    """Cleanup playlists based on PRESERVE setting"""
    try:
        all_playlists = sp.current_user_playlists()['items']
        for playlist in all_playlists:
            if Config.PRESERVE:
                # Only delete playlists created by this script if PRESERVE is True
                if playlist['name'].startswith('ALGO_RESET_'):
                    sp.current_user_unfollow_playlist(playlist['id'])
            else:
                # Delete any playlist if PRESERVE is False
                sp.current_user_unfollow_playlist(playlist['id'])
            time.sleep(SLEEP_BETWEEN_REQUESTS)
    except Exception as e:
        logging.error(f"Error during playlist cleanup: {e}")

if __name__ == "__main__":
    run_continuous_reset()