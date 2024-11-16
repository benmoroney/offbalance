# Configuration

## Core Settings
python

class Config:
# Duration
END_DATE = datetime.now() + timedelta(days=7)
# Sleep Patterns
MIN_SLEEP_DURATION = 1800 # 30 minutes
MAX_SLEEP_DURATION = 14400 # 4 hours
FORCED_SLEEP_START = 4 # 4 AM
FORCED_SLEEP_END = 6 # 6 AM
# Protection
PRESERVE = True # Protect user playlists
# API Limits
MAX_TRACKS_PER_REQUEST = 50
SLEEP_BETWEEN_REQUESTS = 0.1

## Probability Weights
python

WEIGHTS = {
'playlist_creation_chance': 0.4, # 40% chance
'playlist_deletion_chance': 0.3, # 30% chance
'track_interaction_chance': 0.6, # 60% chance
'market_switching_chance': 0.5, # 50% chance
'genre_switching_chance': 0.4 # 40% chance
}

## Environment Variables
Required variables in `.env`:
- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `REDIRECT_URI`
- `WEATHER_API_KEY`

## Advanced Configuration
python

### API rate limiting
MAX_REQUESTS_PER_HOUR = 1000
RETRY_ATTEMPTS = 3
BACKOFF_FACTOR = 2

### Session management
MIN_SESSION_LENGTH = 900 # 15 minutes
MAX_SESSION_LENGTH = 7200 # 2 hours

[Back to Main Documentation](../README.md)
