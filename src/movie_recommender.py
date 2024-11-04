from fuzzywuzzy import process

class MovieRecommender:
    def __init__(self, movies_df, similarity_matrix):
        self.movies_df = movies_df
        self.similarity_matrix = similarity_matrix

    def get_recommendations(self, movie_title, num_recommendations=5):
        """Get movie recommendations based on title"""
        # Find closest matching movie title
        matched_title = process.extractOne(movie_title, self.movies_df['original_title'])[0]
        
        # Get movie index
        movie_index = self.movies_df[self.movies_df['original_title'] == matched_title].index[0]
        
        # Get similarity scores and indices of top movies
        similarity_scores = list(enumerate(self.similarity_matrix[movie_index]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N recommendations
        recommendations = []
        for i in similarity_scores[1:num_recommendations+1]:
            recommendations.append(self.movies_df.iloc[i[0]]['original_title'])
            
        return recommendations 