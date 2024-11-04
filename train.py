import pandas as pd
import pickle
from src.data_processor import process_movies_data, create_similarity_matrix
import os

def train_model():
    print("Starting movie recommendation model training...")
    
    # Check if data files exist
    if not os.path.exists('data/tmdb_5000_movies.csv') or not os.path.exists('data/tmdb_5000_credits.csv'):
        print("Error: Required data files not found!")
        print("Please ensure you have following files in data/ directory:")
        print("1. tmdb_5000_movies.csv")
        print("2. tmdb_5000_credits.csv")
        return
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        print("Loading datasets...")
        movies_df = pd.read_csv('data/tmdb_5000_movies.csv')
        credits_df = pd.read_csv('data/tmdb_5000_credits.csv')
        
        print("Processing and cleaning data...")
        processed_movies = process_movies_data(movies_df, credits_df)
        
        print("Creating similarity matrix...")
        similarity_matrix = create_similarity_matrix(processed_movies)
        
        print("Saving models...")
        with open('data/movie_model.pkl', 'wb') as f:
            pickle.dump(processed_movies, f)
            
        with open('data/matrix_data.pkl', 'wb') as f:
            pickle.dump(similarity_matrix, f)
            
        print("\nTraining completed successfully!")
        print("\nModel files created:")
        print("1. data/movie_model.pkl")
        print("2. data/matrix_data.pkl")
        print("\nNow you can run the streamlit app using: streamlit run app.py")
        
    except Exception as e:
        print(f"Error during training: {e}")

if __name__ == "__main__":
    train_model() 