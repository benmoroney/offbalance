# Troubleshooting

## Common Issues & Solutions

### 1. Authentication Errors
python

**Error**: "Invalid token"
**Solution**:
1. Check .env file configuration
2. Delete .cache file
3. Re-authenticate

### 2. Rate Limiting
python

**Error: "429 Too Many Requests"**
Solution:

1. Increase SLEEP_BETWEEN_REQUESTS
2. Decrease MAX_TRACKS_PER_REQUEST
3. Check current values:
   - Current: 0.1s between requests
   - Try: 0.2s or higher

### 3. Playlist Operation Failures
python

**Error: "Playlist operation failed"**
Check:
1. PRESERVE setting
2. User permissions
3. Network connection
4. Spotify API status

## Debug Mode
python

import logging
logging.basicConfig(
level=logging.DEBUG,
format='%(asctime)s - %(levelname)s - %(message)s'


## Quick Fixes

### Reset Authentication
1. Delete `.cache` file
2. Restart script
3. Re-authenticate

### Network Issues
1. Check internet connection
2. Verify API endpoint status
3. Test with minimal requests

### Memory Issues
1. Reduce batch sizes
2. Clear temporary storage
3. Monitor system resources

[Back to Main Documentation](../README.md)
)
