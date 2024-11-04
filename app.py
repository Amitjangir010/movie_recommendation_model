import streamlit as st
import requests
from src.utils import load_model, download_nltk_data, fetch_poster, fetch_movie_details
from src.movie_recommender import MovieRecommender

# Page config
st.set_page_config(
    page_title="Movie Recommender 🎬",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS with modal styling
st.markdown("""
    <style>
    .movie-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px;
        border-radius: 10px;
        background-color: #1F1F1F;
        margin: 10px;
        transition: transform 0.2s;
    }
    .movie-container:hover {
        transform: scale(1.02);
    }
    .movie-title {
        color: #ffffff;
        font-size: 1.2em;
        margin: 10px 0;
        text-align: center;
    }
    .movie-details {
        color: #cccccc;
        font-size: 0.9em;
        text-align: center;
    }
    .rating {
        color: #ffd700;
        font-weight: bold;
    }
    .modal {
        background-color: #2C2C2C;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .modal-header {
        color: #ffffff;
        border-bottom: 1px solid #444;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .modal-content {
        color: #cccccc;
    }
    .detail-row {
        display: flex;
        margin: 10px 0;
        padding: 5px 0;
        border-bottom: 1px solid #333;
    }
    .detail-label {
        width: 120px;
        color: #888;
    }
    .detail-value {
        flex: 1;
        color: #fff;
    }
    .badge {
        background-color: #444;
        padding: 3px 8px;
        border-radius: 12px;
        margin: 2px;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# Download NLTK data if needed
download_nltk_data()

# Load models
movies_df = load_model('data/movie_model.pkl')
similarity_matrix = load_model('data/matrix_data.pkl')

# Initialize recommender
recommender = MovieRecommender(movies_df, similarity_matrix)

# Sidebar filters
st.sidebar.title("Filters")
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0, 0.5)
genres = st.sidebar.multiselect(
    "Select Genres",
    ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller", "Romance", "Adventure"]
)

# Main content
st.title('🎬 Movie Recommendation System')
st.markdown("""
    <p style='font-size: 1.2em; color: #cccccc;'>
    Discover movies similar to your favorites! Enter a movie name below and get personalized recommendations.
    </p>
    """, unsafe_allow_html=True)

# Search box with autocomplete
movie_list = movies_df['original_title'].tolist()
movie_name = st.selectbox('Enter Movie Name:', movie_list)

if st.button('Get Recommendations', key='recommend_btn'):
    try:
        with st.spinner('Finding recommendations...'):
            recommendations = recommender.get_recommendations(movie_name, num_recommendations=6)
            
            # Display input movie
            st.subheader('Selected Movie:')
            col1, col2 = st.columns([1, 3])
            
            # Fetch and display input movie details
            movie_id = movies_df[movies_df['original_title'] == movie_name]['id'].iloc[0]
            poster_url = fetch_poster(movie_id)
            movie_details = fetch_movie_details(movie_id)
            
            with col1:
                if poster_url:
                    st.image(poster_url, width=200)
                else:
                    st.image("placeholder.jpg", width=200)
                    
            with col2:
                st.markdown(f"""
                    <div style='padding: 20px;'>
                        <h3>{movie_name}</h3>
                        <p><span class='rating'>⭐ {movie_details['rating']}</span> | {movie_details['year']}</p>
                        <p>{movie_details['overview'][:200]}...</p>
                        <p><b>Genres:</b> {', '.join(movie_details['genres'])}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Display recommendations
            st.subheader('Recommended Movies:')
            cols = st.columns(3)
            
            # Store movie details in session state
            if 'movie_details' not in st.session_state:
                st.session_state.movie_details = {}
            if 'selected_movie' not in st.session_state:
                st.session_state.selected_movie = None
            
            for idx, (movie, col) in enumerate(zip(recommendations, cols * 2)):
                movie_id = movies_df[movies_df['original_title'] == movie]['id'].iloc[0]
                poster_url = fetch_poster(movie_id)
                details = fetch_movie_details(movie_id)
                
                # Store details in session state
                st.session_state.movie_details[f'movie_{idx}'] = details
                
                # Filter based on rating and genres
                if details['rating'] >= min_rating and (not genres or any(g in details['genres'] for g in genres)):
                    with col:
                        # Movie container with clickable area
                        movie_container = st.container()
                        with movie_container:
                            st.markdown(f"""
                                <div class='movie-container'>
                                    <img src='{poster_url if poster_url else "placeholder.jpg"}' width='200'>
                                    <div class='movie-title'>{movie}</div>
                                    <div class='movie-details'>
                                        ⭐ {details['rating']} | {details['year']}<br>
                                        {', '.join(details['genres'][:3])}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Create expander for movie details
                            with st.expander("Show Details 🎬"):
                                movie_detail = details
                                st.markdown(f"""
                                    <div class='modal'>
                                        <div class='modal-header'>
                                            <h2>{movie}</h2>
                                        </div>
                                        <div class='modal-content'>
                                            <div class='detail-row'>
                                                <div class='detail-label'>Rating</div>
                                                <div class='detail-value'>⭐ {movie_detail['rating']}/10</div>
                                            </div>
                                            <div class='detail-row'>
                                                <div class='detail-label'>Year</div>
                                                <div class='detail-value'>{movie_detail['year']}</div>
                                            </div>
                                            <div class='detail-row'>
                                                <div class='detail-label'>Runtime</div>
                                                <div class='detail-value'>{movie_detail['runtime']} minutes</div>
                                            </div>
                                            <div class='detail-row'>
                                                <div class='detail-label'>Genres</div>
                                                <div class='detail-value'>
                                                    {''.join([f"<span class='badge'>{g}</span>" for g in movie_detail['genres']])}
                                                </div>
                                            </div>
                                            <div class='detail-row'>
                                                <div class='detail-label'>Director</div>
                                                <div class='detail-value'>{movie_detail['director']}</div>
                                            </div>
                                            <div class='detail-row'>
                                                <div class='detail-label'>Cast</div>
                                                <div class='detail-value'>{', '.join(movie_detail['cast'][:5])}</div>
                                            </div>
                                            <div style='margin-top: 15px;'>
                                                <h4>Overview</h4>
                                                <p>{movie_detail['overview']}</p>
                                            </div>
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                    
    except Exception as e:
        st.error('Error: Could not find similar movies. Please try another movie name.')

# Footer
st.markdown("""
    <div style='text-align: center; color: #666666; padding: 20px;'>
        Made with ❤️ by Amit Jangir | Data from TMDB
    </div>
    """, unsafe_allow_html=True)