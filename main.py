from fastapi import FastAPI
from recommend import CourseRecommender
import uvicorn

# 1. Initialize the App
app = FastAPI(
    title="Course Recommender API",
    description="An API that suggests courses based on cosine similarity.",
    version="1.0"
)

# 2. Load the Model (The "Brain") once when the server starts
recommender = CourseRecommender()

# 3. Create the API Endpoint
# This is the "Door" that the frontend will knock on
@app.get("/recommend")
def get_recommendations(course_name: str):
    results = recommender.get_recommendations(course_name)
    
    if results is None:
        return {"error": "Course not found. Please try another name."}
    
    return {"recommendations": results}

# 4. Run the Server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)