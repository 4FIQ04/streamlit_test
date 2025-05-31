import streamlit as st
import requests
import pandas as pd
import altair as alt

# ========== Streamlit UI Setup ==========
st.set_page_config(page_title="🎬 TMDb Movie Explorer", layout="centered")
st.title("🎥 TMDb Movie Explorer App")
st.markdown("Search movies by title and explore ratings, genres, and details.")

# ========== User Input ==========
api_key = st.text_input("Enter your TMDb API key:", type="password")
query = st.text_input("Enter a movie title:", "Inception")

# ========== TMDb API Call Functions ==========

def search_movie(query, api_key):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    response = requests.get(url)
    return response.json()

def get_movie_details(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json()

# ========== Fetch and Display Data ==========
if st.button("Search Movie"):
    if not api_key:
        st.warning("⚠️ Please enter your TMDb API key.")
    else:
        search_result = search_movie(query, api_key)

        if "results" not in search_result or len(search_result["results"]) == 0:
            st.error("❌ No movie found with that title.")
        else:
            movie = search_result["results"][0]
            movie_id = movie["id"]
            details = get_movie_details(movie_id, api_key)

            # ========== Movie Info ==========
            st.subheader(f"🎞️ {details['title']} ({details['release_date'][:4]})")
            st.image(f"https://image.tmdb.org/t/p/w500{details['poster_path']}")
            st.markdown(f"**Overview**: {details['overview']}")
            st.markdown(f"**Runtime**: {details['runtime']} mins")
            st.markdown(f"**Vote Average**: {details['vote_average']}")
            st.markdown(f"**Total Votes**: {details['vote_count']}")

            # ========== Visualization 1: Vote Rating vs Count ==========
            vote_data = pd.DataFrame({
                "Metric": ["Average Rating", "Vote Count"],




