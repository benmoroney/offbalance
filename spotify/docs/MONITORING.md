# Monitoring & Logs

## Log File Structure
plaintext

spotify_reset_YYYYMMDD_HHMMSS.log

### Contents:
[TIMESTAMP] - INFO - Starting week-long algorithm reset
[TIMESTAMP] - INFO - Created playlist: ALGO_RESET_Morning_...
[TIMESTAMP] - INFO - Collected 500 tracks from market US
[TIMESTAMP] - WARNING - Rate limit approaching
[TIMESTAMP] - ERROR - Failed to create playlist: ...

## Key Metrics to Monitor

### 1. Session Information
- Duration
- Activities performed
- Success rates
- Sleep patterns

### 2. Track Statistics
- Number of tracks collected
- Interaction counts
- Market distribution
- Genre distribution

### 3. Error Rates
- API failures
- Rate limiting hits
- Connection issues
- Recovery attempts

## Monitoring Tools

### 1. Built-in Logging
python

logging.basicConfig(
filename=f'spotify_reset_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s'
)

### 2. Status Checks
python

def check_status():
return {
'uptime': get_uptime(),
'tracks_processed': track_counter,
'playlists_created': playlist_counter,
'errors': error_counter
}

[Back to Main Documentation](../README.md)
