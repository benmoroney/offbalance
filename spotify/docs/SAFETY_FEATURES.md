# Safety Features

## PRESERVE Mode
When `PRESERVE = True`:
python

Protected Items:
✓ User-created playlists
✓ Followed playlists
✓ Collaborative playlists
✓ Saved/liked playlists

## Content Identification
python

### Playlist naming convention
f"ALGO_RESET_{context}{timestamp}{id}"

Example Names:
ALGO_RESET_Morning_20240315_123456_001
ALGO_RESET_Discover_20240315_123456_002


## Rate Limiting Protection
python

### Built-in protections
MAX_REQUESTS_PER_HOUR = 1000
SLEEP_BETWEEN_REQUESTS = 0.1 # seconds

### Automatic throttling
if requests_this_hour >= MAX_REQUESTS_PER_HOUR:
sleep_until_next_hour()

## Error Handling

mermaid
graph TD
A[Error Occurs] --> B[Log Error]
B --> C[Sleep 5 Minutes]
C --> D[Resume Operation]
D --> E{Critical Error?}
E -->|Yes| F[Graceful Shutdown]
E -->|No| G[Continue]


[Back to Main Documentation](../README.md)
