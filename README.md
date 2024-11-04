# 🎬 Movie Recommendation System

A sophisticated content-based movie recommendation system that leverages machine learning to provide personalized movie suggestions.

## ✨ Key Features

- 🔍 Intelligent search with autocomplete functionality
- 🎯 Content-based recommendation engine
- 🌟 Dynamic movie information display
- 📝 Comprehensive movie metadata
- ⚡ Optimized performance
- 🎨 Modern, responsive interface
- 🎯 Advanced filtering capabilities

## 🚀 Getting Started

### System Requirements
- Python 3.7 or higher
- Internet connectivity for API access

### Installation Guide 🛠️

1. **Clone the repository:**   ``
   git clone https://github.com/Amitjangir010/movie_recommendation_model.git
  ``

2. **Configure virtual environment:**  
   python -m venv venv
   
   # For Windows:
   venv\Scripts\activate
   
   # For Linux/Mac:
   source venv/bin/activate

3. **Install dependencies:**   ```
   pip install -r requirements.txt   ```

4. **Configure TMDB API:**
   - Register at [TMDB website](https://www.themoviedb.org/settings/api)
   - Generate API key
   - Create `.env` file in project root
   - Configure API key:     ```
     TMDB_API_KEY=your_api_key_here     ```

5. **Dataset Configuration:**
   - Download required files from [Kaggle TMDB 5000 Dataset](https://www.kaggle.com/tmdb/tmdb-movie-metadata):
     - tmdb_5000_movies.csv
     - tmdb_5000_credits.csv
   - Place files in `data/` directory

6. **Model Training:**   ```
   python train.py   ```

7. **Application Launch:**   ```
   streamlit run app.py   ```

## 🎮 Usage Instructions

1. **Search Functionality:** Enter movie title in search field
2. **Filter Application:** Utilize sidebar for rating and genre filtering
3. **Generate Recommendations:** Click "Get Recommendations"
4. **Detailed Information:** Access comprehensive movie details via expander

## 🎯 System Features

### 🔍 Search Engine
- Fuzzy string matching implementation
- Autocomplete functionality
- Efficient search algorithm

### 🎨 User Interface
- High-resolution movie posters
- Interactive rating system
- Intuitive layout design
- Dark mode optimization
- Responsive design implementation

### 📊 Filtering System
- Rating-based filtration
- Genre-specific filtering
- Quality metrics implementation

### 📝 Information Display
- Comprehensive movie synopsis
- Cast information
- Director details
- Release information
- Runtime statistics
- User rating metrics

## 🛠️ Technical Framework

- Streamlit (UI Framework)
- Pandas & NumPy (Data Processing)
- Scikit-learn (ML Implementation)
- TMDB API (Data Source)
- NLTK (Text Processing)
- Python-dotenv (Environment Management)

## 📝 Important Information

- Initial NLTK data download necessary
- Internet connectivity required for poster display

## 💡 Optimization Tips

- Experiment with genre combinations
- Adjust rating thresholds
- Explore detailed movie information
- Maintain regular updates

## 🙏 Acknowledgments

- TMDB API services
- Kaggle dataset
- Open source community

---
Developed with precision by Amit Jangir | Powered by TMDB
