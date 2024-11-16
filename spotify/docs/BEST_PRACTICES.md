# Best Practices

## 1. Running the Script

### Recommended Setup
bash

### Run in screen or tmux session
screen -S spotify_reset
python spotify_randomizer.py

### Ctrl+A+D to detach
#### Return to session
screen -r spotify_reset

### Optimal Configuration
python

Recommended Settings:
- PRESERVE = True # First run
- Run during low-usage hours
- Monitor for first 24 hours
- Adjust sleep times based on API response

  
## 2. Pre-Run Checklist
✅ Backup important playlists
✅ Check API quotas
✅ Verify network stability
✅ Set up monitoring
✅ Review logs location

## 3. During Operation
📊 Monitor logs regularly
🔍 Check Spotify account activity
⏰ Note any pattern changes
🚫 Don't manually modify script-created playlists

## 4. Post-Run Actions
1. Review logs for insights
2. Clean up remaining temporary playlists
3. Document changes in recommendations
4. Wait 2-3 weeks for full algorithm adjustment

[Back to Main Documentation](../README.md)
