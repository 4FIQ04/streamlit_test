import streamlit as st
import requests
import pandas as pd
import altair as alt

# ========== Streamlit UI Setup ==========
st.set_page_config(page_title="🎬 Movie Explorer", layout="centered")

# ========== Dark Animated Background ==========
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #c6f0e2, #ffe0d2);
        color: #333;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 20px;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #222 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ========== App Title ==========
st.title("🎥 :rainbow[Movie Explorer App]")
st.markdown("Search movies by title and explore storyline, director, stars, stats, and trailer.")

# ========== User Name Input ==========
user_name = st.text_input("Enter your name:", "Guest")
st.markdown(f"👋 Hello, *{user_name}*! Let's explore some movies.")

# ========== Developer API Key ==========
API_KEY = "4f658b3a4df357c0e36dea39fe745497"  # Replace with your TMDb API key

# ========== Movie Title Input ==========
query = st.text_input("Enter a movie title:", "Sheriff: Narko Integriti")

# ========== TMDb API Call Functions ==========
def search_movie(query, api_key):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    return requests.get(url).json()

def get_movie_details(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    return requests.get(url).json()

def get_movie_credits(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
    return requests.get(url).json()

# ========== NEW: Get Movie Trailer ==========
def get_movie_trailer(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
    videos = requests.get(url).json().get("results", [])
    for video in videos:
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

# ========== Fetch and Display Data ==========
if st.button("Search Movie"):
    search_result = search_movie(query, API_KEY)

    if "results" not in search_result or len(search_result["results"]) == 0:
        st.error("❌ No movie found with that title.")
    else:
        movie = search_result["results"][0]
        movie_id = movie["id"]
        details = get_movie_details(movie_id, API_KEY)
        credits = get_movie_credits(movie_id, API_KEY)
        trailer_url = get_movie_trailer(movie_id, API_KEY)  # NEW

        # Get director
        director = "Unknown"
        for member in credits.get("crew", []):
            if member["job"] == "Director":
                director = member["name"]
                break

        # Get top 3 actors
        cast_list = credits.get("cast", [])
        top_cast = ", ".join([actor["name"] for actor in cast_list[:3]]) if cast_list else "N/A"

        # ========== Movie Info ==========
        st.subheader(f"🎞 {details['title']} ({details['release_date'][:4]})")
        if details.get("poster_path"):
            st.image(f"https://image.tmdb.org/t/p/w500{details['poster_path']}")
        st.markdown(f"*Storyline*: {details.get('overview', 'No overview available.')}")
        st.markdown(f"*Director*: {director}")
        st.markdown(f"*Stars*: {top_cast}")
        st.markdown(f"*Runtime*: {details.get('runtime', 'N/A')} mins")
        st.markdown(f"*Vote Average*: {details['vote_average']}")
        st.markdown(f"*Total Votes*: {details['vote_count']}")

        # ========== NEW: Movie Trailer Section ==========
        if trailer_url:
            st.subheader("🎬 Watch Trailer")
            st.video(trailer_url)
        else:
            st.info("No trailer available for this movie.")

        # ========== Visualization 1: Vote Rating vs Count ==========
        vote_data = pd.DataFrame({
            "Metric": ["Average Rating", "Vote Count"],
            "Value": [details["vote_average"], details["vote_count"]]
        })

        st.subheader("📊 Rating and Vote Count")
        bar_chart = alt.Chart(vote_data).mark_bar().encode(
            x="Metric",
            y="Value",
            color=alt.Color("Metric", scale=alt.Scale(scheme='dark2')),
            tooltip=["Metric", "Value"]
        ).properties(width=600)
        st.altair_chart(bar_chart)

        # ========== Visualization 2: Genre Breakdown ==========
        genres = [g["name"] for g in details["genres"]]
        genre_df = pd.DataFrame({"Genre": genres, "Count": [1]*len(genres)})

        st.subheader("🎨 Genre Breakdown")
        pie_chart = alt.Chart(genre_df).mark_arc().encode(
            theta="Count",
            color=alt.Color("Genre", scale=alt.Scale(scheme='tableau10')),
            tooltip="Genre"
        )
        st.altair_chart(pie_chart)

        # ========== User Review Section ==========
        st.markdown("---")
        st.subheader("📝 Your Review")

        # Initialize session state
        if "submitted" not in st.session_state:
            st.session_state["submitted"] = False
        if "saved_review" not in st.session_state:
            st.session_state["saved_review"] = ""
        if "saved_rating" not in st.session_state:
            st.session_state["saved_rating"] = 0

        # Input widgets
        user_review = st.text_area("Write your review here (optional):", "")
        star_options = list(range(0, 6))
        star_rating = st.radio(
            "Rate this movie:",
            options=star_options,
            format_func=lambda x: "⭐" * x + "☆" * (5 - x),
            horizontal=True
        )

        # Submit button
        if st.button("Submit Review"):
            st.session_state["submitted"] = True
            st.session_state["saved_review"] = user_review
            st.session_state["saved_rating"] = star_rating
            st.success("✅ Thank you for your review!")

        # Show saved review
        if st.session_state["submitted"]:
            st.markdown(f"👤 **Reviewed by:** {user_name}")
            st.markdown(f"⭐ **Your Rating:** {st.session_state['saved_rating']} / 5")
            if st.session_state["saved_review"].strip():
                st.markdown(f"📝 **Your Review:** {st.session_state['saved_review']}")
            else:
                st.markdown("No written review provided.")
