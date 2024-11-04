import pickle
import nltk
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TMDB API configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'your_tmdb_api_key_here')
TMDB_BASE_URL = "https://api.themoviedb.org/3"

def download_nltk_data():
    """Download required NLTK data"""
    try:
        nltk.download('punkt', quiet=True)
    except Exception as e:
        print(f"Warning: Could not download NLTK data: {e}")

def load_model(model_path):
    """Load pickle model"""
    with open(model_path, 'rb') as f:
        return pickle.load(f)

def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API"""
    try:
        response = requests.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}",
            params={'api_key': TMDB_API_KEY}
        )
        data = response.json()
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    except:
        return None

def fetch_movie_details(movie_id):
    """Fetch detailed movie information from TMDB API"""
    try:
        # Fetch movie details
        response = requests.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}",
            params={
                'api_key': TMDB_API_KEY,
                'append_to_response': 'credits'
            }
        )
        data = response.json()
        
        return {
            'title': data['title'],
            'overview': data['overview'],
            'genres': [g['name'] for g in data['genres']],
            'rating': round(data['vote_average'], 1),
            'year': data['release_date'][:4],
            'cast': [c['name'] for c in data['credits']['cast']],
            'director': next((c['name'] for c in data['credits']['crew'] if c['job'] == 'Director'), 'N/A'),
            'runtime': data['runtime'],
            'language': data['original_language']
        }
    except:
        return {
            'title': 'N/A',
            'overview': 'No overview available',
            'genres': [],
            'rating': 0.0,
            'year': 'N/A',
            'cast': [],
            'director': 'N/A',
            'runtime': 0,
            'language': 'N/A'
        }