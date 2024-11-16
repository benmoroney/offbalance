# How It Works

## 1. Session Management

### Time-Based Operation

mermaid

flowchart TD
    %% Initialization
    Start["Script Start"] --> Init["Initialize"]
    Init --> Auth["Spotify Authentication"]
    Auth --> GetUser["Get User Info"]
    GetUser --> ConfigInit["Initialize Config:\n- PRESERVE setting\n- Sleep times\n- Session lengths\n- API limits\n- Week duration"]
    
    %% Main Loop
    ConfigInit --> MainLoop["Start Main Loop"]
    MainLoop --> WeekCheck{"Week\nOver?"}
    WeekCheck -->|"Yes"| EndScript["End Script"]
    WeekCheck -->|"No"| TimeCheck
    
    %% Time Checking
    TimeCheck{"Check Time"} -->|"4-6 AM"| ForcedSleep["Force Sleep Until 6 AM"]
    TimeCheck -->|"Other Hours"| RandomSleep{"Random Sleep?\n30% Chance"}
    
    RandomSleep -->|"Yes"| Sleep["Sleep 30min-4hrs"]
    RandomSleep -->|"No"| Session["Start New Session"]
    
    %% Session Setup
    Session --> RandomizeWeights["Randomize All Weights:\n- Playlist creation\n- Track interaction\n- Market switching\n- Genre switching"]
    
    %% Context Collection
    RandomizeWeights --> GetContext["Collect Context Data:\n- Location\n- Weather\n- Time\n- Day type"]
    
    %% Preservation Check
    GetContext --> PreserveCheck{"PRESERVE\nEnabled?"}
    
    PreserveCheck -->|"Yes"| Protected["Protected Mode:\n- Only script playlists\n- Mark new playlists\n- Skip user content"]
    PreserveCheck -->|"No"| Unrestricted["Unrestricted Mode:\n- All playlists\n- No protection\n- Full access"]
    
    %% Action Execution
    Protected & Unrestricted --> Actions["Execute Random Actions"]
    
    subgraph "Session Activities"
        Actions --> Playlists["Playlist Management\n- Create (40% chance)\n- Delete (30% chance)\n- Add/Remove tracks"]
        
        Actions --> Markets["Market Operations\n- Switch markets (50% chance)\n- Get regional content"]
        
        Actions --> Tracks["Track Collection\n- Featured playlists\n- Different markets\n- Random genres\n- Recommendations\n- User playlists"]
        
        Actions --> TrackAttr["Track Attributes\n- Tempo\n- Energy\n- Danceability\n- Acousticness\n- Valence\n- All randomized"]
        
        Actions --> Interact["Track Interactions\n- Like/Unlike\n- Add to queue\n- Play/Skip\n- Random durations\n- Random delays"]
    end
    
    %% Session Control
    Actions --> TimeUp{"Session\nTime Up?"}
    TimeUp -->|"No"| Actions
    TimeUp -->|"Yes"| PostSession["Post-Session Actions"]
    
    %% Error Handling
    Session --> Error["Error Occurs"]
    Error --> LogError["Log Error"]
    LogError --> ErrorSleep["Sleep 5min"]
    
    %% Cleanup and Continue
    PostSession --> Cleanup["Cleanup:\n- Remove temp playlists\n- Log activities"]
    ErrorSleep --> MainLoop
    Cleanup --> MainLoop
    ForcedSleep --> MainLoop
    Sleep --> MainLoop
    
    %% Shutdown Handling
    MainLoop --> Interrupt{"Interrupt\nReceived?"}
    Interrupt -->|"Yes"| GracefulStop["Graceful Shutdown:\n- Cleanup\n- Log completion\n- Save state"]
    GracefulStop --> EndScript
    Interrupt -->|"No"| MainLoop


### Session Activities Table
| Activity | Chance | Description |
|----------|---------|-------------|
| Create Playlist | 40% | Creates new randomized playlist |
| Switch Market | 50% | Changes regional context |
| Collect Tracks | 100% | Gathers tracks from various sources |
| Interact | 60% | Likes, plays, or skips tracks |
| Cleanup | 30% | Removes temporary playlists |

## 2. Track Selection Process

### Collection Methods
python

def get_massive_track_collection():
1️⃣ Featured Playlists
2️⃣ Market-Specific Tracks
3️⃣ Genre-Based Recommendations
4️⃣ Random Attributes
5️⃣ User Collection (if PRESERVE=False)


### Track Attributes
All track selections consider random values for:
- 🎵 Tempo (50-200 BPM)
- 🔊 Energy (0.0-1.0)
- 💃 Danceability (0.0-1.0)
- 🎸 Instrumentalness (0.0-1.0)
- 🎭 Valence (0.0-1.0)
- 📢 Loudness (-60.0-0.0 dB)

[Back to Main Documentation](../README.md)
