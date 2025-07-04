import streamlit as st
import requests
import pandas as pd
import altair as alt

# ========== Streamlit UI Setup ==========
st.set_page_config(page_title="🎬 Movie Explorer", layout="centered")

# ========== Background Styling ==========
st.markdown("""
    <style>
    body {
        background: linear-gradient(-45deg, #a8dadc, #f1faee, #caf0f8, #e0f7fa);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #000000;
    }
    .stApp {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        font-family: 'Segoe UI', sans-serif;
        color: #000000;
    }
    h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #000000 !important;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    </style>
""", unsafe_allow_html=True)

# ========== App Title ==========
st.title("🎥 :rainbow[Movie Explorer App]")
st.markdown("Search movies by title or browse categories. Explore storyline, stats, trailer, and submit a review.")

# ========== User Name ==========
user_name = st.text_input("Enter your name:", "Guest")
st.markdown(f"👋 Hello, *{user_name}*! Let's explore some movies.")

# ========== TMDb API ==========
API_KEY = "4f658b3a4df357c0e36dea39fe745497"  # Replace with your own TMDb API key

# ========== Movie Search ==========
query = st.text_input("Enter a movie title:", "")

# ========== Category Dropdown ==========
st.markdown("## 🎯 Browse by Category")
category = st.selectbox("Or select a category:", ["Popular", "Now Playing", "Upcoming", "Top Rated"])
category_map = {
    "Popular": "popular",
    "Now Playing": "now_playing",
    "Upcoming": "upcoming",
    "Top Rated": "top_rated"
}

# ========== TMDb API Functions ==========
def search_movie(query, api_key):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    return requests.get(url).json()

def get_movie_details(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    return requests.get(url).json()

def get_movie_credits(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}"
    return requests.get(url).json()

def get_movie_trailer(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
    videos = requests.get(url).json().get("results", [])
    for video in videos:
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

def get_movies_by_category(category_key, api_key):
    url = f"https://api.themoviedb.org/3/movie/{category_key}?api_key={api_key}&language=en-US&page=1"
    return requests.get(url).json().get("results", [])

# ========== Rating Options ==========
rating_options = {
    "☆☆☆☆☆ (0)": 0,
    "⭐☆☆☆☆ (1)": 1,
    "⭐⭐☆☆☆ (2)": 2,
    "⭐⭐⭐☆☆ (3)": 3,
    "⭐⭐⭐⭐☆ (4)": 4,
    "⭐⭐⭐⭐⭐ (5)": 5
}
rating_labels = list(rating_options.keys())
default_index = 5

# ========== Main Logic ==========
if query.strip() == "":
    st.markdown(f"### 🎞 {category} Movies")
    movies = get_movies_by_category(category_map[category], API_KEY)
    cols = st.columns(3)
    for i, movie in enumerate(movies[:9]):
        with cols[i % 3]:
            st.markdown(f"**{movie['title']}**")
            if movie.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w200{movie['poster_path']}", use_container_width=True)
            st.caption(movie.get("overview", "No overview available."))
else:
    search_result = search_movie(query, API_KEY)

    if "results" not in search_result or len(search_result["results"]) == 0:
        st.error("❌ No movie found with that title.")
    else:
        movie_options = [
            f"{m['title']} ({m.get('release_date', 'N/A')[:4]})"
            for m in search_result["results"] if m.get("release_date")
        ]

        selected_title = st.selectbox("Select a movie for more details:", movie_options)

        if selected_title:
            selected_index = movie_options.index(selected_title)
            movie = search_result["results"][selected_index]
            movie_id = movie["id"]

            details = get_movie_details(movie_id, API_KEY)
            credits = get_movie_credits(movie_id, API_KEY)
            trailer_url = get_movie_trailer(movie_id, API_KEY)

            director = next((m["name"] for m in credits.get("crew", []) if m["job"] == "Pengarah"), "Unknown")
            cast_list = credits.get("cast", [])
            top_cast = ", ".join([actor["name"] for actor in cast_list[:3]]) if cast_list else "N/A"

            st.subheader(f"🎞 {details['title']} ({details.get('release_date', '')[:4]})")
            if details.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w500{details['poster_path']}")
            st.markdown(f"*Storyline*: {details.get('overview', 'No overview available.')}")
            st.markdown(f"*Pengarah*: {director}")
            st.markdown(f"*Stars*: {top_cast}")
            st.markdown(f"*Runtime*: {details.get('runtime', 'N/A')} mins")
            st.markdown(f"*Vote Average*: {details['vote_average']}")
            st.markdown(f"*Total Votes*: {details['vote_count']}")

            if trailer_url:
                st.subheader("🎬 Watch Trailer")
                st.video(trailer_url)
            else:
                st.info("No trailer available.")

            st.subheader("📆 Movie Release Year Comparison")
            compare_df = pd.DataFrame([{
                "Title": m["title"],
                "Year": m.get("release_date", "N/A")[:4] if m.get("release_date") else "N/A"
            } for m in search_result["results"] if m.get("release_date")])
            st.table(compare_df)

            st.subheader("📊 Rating and Vote Count")
            vote_data = pd.DataFrame({
                "Metric": ["Average Rating", "Vote Count"],
                "Value": [details["vote_average"], details["vote_count"]]
            })
            st.altair_chart(
                alt.Chart(vote_data).mark_bar().encode(
                    x="Metric",
                    y="Value",
                    color=alt.Color("Metric", scale=alt.Scale(scheme='dark2')),
                    tooltip=["Metric", "Value"]
                ).properties(width=600)
            )

            genres = [g["name"] for g in details["genres"]]
            genre_df = pd.DataFrame({"Genre": genres, "Count": [1]*len(genres)})
            st.subheader("🎨 Genre Breakdown")
            if len(genre_df) > 1:
                st.altair_chart(
                    alt.Chart(genre_df).mark_arc().encode(
                        theta="Count",
                        color=alt.Color("Genre", scale=alt.Scale(scheme='tableau10')),
                        tooltip="Genre"
                    )
                )
            elif len(genre_df) == 1:
                st.info(f"Genre: {genres[0]}")

            st.markdown("---")
            st.subheader("📝 Your Review")
            with st.form("review_form"):
                user_review = st.text_area("Write your review here (optional):", "")
                selected_label = st.radio("Rate this movie:", rating_labels, index=default_index, horizontal=True)
                star_rating = rating_options.get(selected_label, 0)
                submitted = st.form_submit_button("Submit Review")
                if submitted:
                    st.success("✅ Thank you for your review!")
                    st.markdown(f"👤 Reviewed by: **{user_name}**")
                    st.markdown(f"⭐ Your Rating: **{star_rating} / 5**")
                    if user_review.strip():
                        st.markdown(f"📝 Your Review: **{user_review}**")
                    else:
                        st.markdown("No written review provided.")


