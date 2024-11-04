import pandas as pd
import numpy as np
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ps = PorterStemmer()

def tag_genres(genre):
    """Extract genre names from JSON string"""
    return [i["name"] for i in ast.literal_eval(genre)]

def tag_cast(cast):
    """Extract first 3 cast names from JSON string"""
    cast_list = []
    count = 1
    for i in ast.literal_eval(cast):
        if count < 4:
            cast_list.append(i["name"])
            count += 1
        else:
            break
    return cast_list

def tag_director(crew):
    """Extract director name from crew JSON string"""
    for i in ast.literal_eval(crew):
        if i["job"] == 'Director':
            return [i['name']]
    return []

def stem_words(text):
    """Apply stemming to words"""
    return " ".join([ps.stem(word) for word in text.split()])

def process_movies_data(movies_df, credits_df):
    """Process and transform movies data"""
    print("Merging dataframes...")
    movies = movies_df.merge(credits_df, on='title')
    
    print("Selecting required columns...")
    # Keep only required columns from original notebook
    movies = movies[['genres', 'id', 'keywords', 'original_title', 'overview', 'cast', 'crew']]
    
    print("Cleaning data...")
    movies.dropna(inplace=True)
    
    print("Processing text columns...")
    # Process text columns as per notebook
    movies['genres'] = movies['genres'].apply(tag_genres)
    movies['keywords'] = movies['keywords'].apply(tag_genres)
    movies['cast'] = movies['cast'].apply(tag_cast)
    movies['crew'] = movies['crew'].apply(tag_director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    
    print("Creating tags...")
    # Combine all features
    movies['tags'] = movies['genres'] + movies['cast'] + movies['keywords'] + movies['crew'] + movies['overview']
    movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
    movies['tags'] = movies['tags'].apply(stem_words)
    
    return movies[['id', 'original_title', 'tags']]

def create_similarity_matrix(movies_df):
    """Create cosine similarity matrix"""
    print("Creating count vectors...")
    cv = CountVectorizer(max_features=6000, stop_words='english')
    vectors = cv.fit_transform(movies_df['tags']).toarray()
    
    print("Calculating similarity matrix...")
    return cosine_similarity(vectors) 