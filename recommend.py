import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class CourseRecommender:
    def __init__(self):
        # 1. Load Data
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, "data", "courses.csv")
        
        self.df = pd.read_csv(data_path)
        
        # 2. Data Cleaning
        # UPDATED: Using the correct column name 'name'
        self.df = self.df.dropna(subset=['name'])
        self.df = self.df.drop_duplicates(subset=['name'])
        self.df = self.df.reset_index(drop=True)

        # 3. Feature Engineering
        # UPDATED: Since we don't have a description, we combine 'name' + 'institution'
        self.df['tags'] = self.df['name'] + " " + self.df['institution']
        self.df['tags'] = self.df['tags'].astype(str).str.lower()

        # 4. Vectorization
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.vectors = self.vectorizer.fit_transform(self.df['tags'])

        # 5. Similarity Matrix
        self.similarity = cosine_similarity(self.vectors)

    def get_recommendations(self, course_name, top_k=5):
        # UPDATED: Check if course exists in 'name' column
        if course_name not in self.df['name'].values:
            return None

        # Find index
        course_index = self.df[self.df['name'] == course_name].index[0]
        distances = self.similarity[course_index]
        
        # Sort
        course_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
        course_list = course_list[1:top_k+1]

        recommendations = []
        for i in course_list:
            course_idx = i[0]
            score = i[1]
            recommendations.append({
                "course_name": self.df.iloc[course_idx]['name'],
                "similarity_score": round(score * 100, 2),
                # UPDATED: Showing Institution instead of Difficulty
                "difficulty": self.df.iloc[course_idx]['institution'], 
                "url": self.df.iloc[course_idx]['course_url']
            })
            
        return recommendations

if __name__ == "__main__":
    recommender = CourseRecommender()
    # UPDATED: Use a simpler name found in your dataset
    test_course = "Machine Learning" 
    print(f"Testing Recommendation for: {test_course}")
    results = recommender.get_recommendations(test_course)
    print(results)