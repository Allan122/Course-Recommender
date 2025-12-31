import streamlit as st
import pandas as pd
import requests
import os

# 1. Setup Streamlit Page
st.set_page_config(page_title="Course Recommender", layout="wide")
st.title("📚 AI-Powered Course Recommender")
st.markdown("Select a course you liked, and our AI will suggest similar upskilling options.")

# 2. Load Data (Just to get the list of names for the dropdown)
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "courses.csv")
    df = pd.read_csv(data_path)
    return df['name'].unique()

course_names = load_data()

# 3. User Input
selected_course = st.selectbox("Select a Course:", course_names)

# 4. Button to Get Recommendations
if st.button("Get Recommendations"):
    with st.spinner("Consulting the AI..."):
        try:
            # --- CORRECTED SECTION START ---
            # Notice how these lines are indented inside the 'try' block
            API_URL = "https://allan-course-api.onrender.com"
            response = requests.get(f"{API_URL}/recommend?course_name={selected_course}")
            # --- CORRECTED SECTION END ---
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we got valid recommendations
                if "recommendations" in data:
                    st.success(f"Here are 5 courses similar to **{selected_course}**:")
                    
                    # Display results in a nice grid
                    for item in data["recommendations"]:
                        with st.container():
                            st.subheader(item['course_name'])
                            st.write(f"**Institution:** {item['difficulty']}")
                            st.write(f"**Similarity Score:** {item['similarity_score']}%")
                            st.markdown(f"[View Course]({item['url']})")
                            st.divider()
                else:
                    st.error(data.get("error", "Unknown error"))
            else:
                st.error("Error connecting to the API server.")
                
        except Exception as e:
            st.error(f"Connection Error: {e}. Is your API server running?")