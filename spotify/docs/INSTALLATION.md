# Installation

## 1. Clone or Download

bash

### Option 1: Git Clone
git clone https://your-repository/spotify-algorithm-randomizer.git

### Option 2: Download script directly
Save the script as spotify_randomizer.py

## 2. Install Dependencies

bash

### Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate # Unix/macOS
.\venv\Scripts\activate # Windows

### Install required packages
pip install spotipy requests timezonefinder astral

## 3. Environment Setup
Create a `.env` file in the script directory:

env
SPOTIPY_CLIENT_ID='your_client_id'
SPOTIPY_CLIENT_SECRET='your_client_secret'
REDIRECT_URI='http://localhost:8888/callback'
WEATHER_API_KEY='your_weather_api_key'

## 4. Verify Installation

bash
### Test Python environment
python -c "import spotipy, requests, timezonefinder, astral"

### Test Spotify authentication
python -c "import spotipy; from spotipy.oauth2 import SpotifyOAuth; sp = spotipy.Spotify(auth_manager=SpotifyOAuth())"

## 5. First Run
bash
python spotify_randomizer.py --test


[Back to Main Documentation](../README.md)
