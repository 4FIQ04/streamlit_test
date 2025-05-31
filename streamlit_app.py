import streamlit as st
import requests
import pandas as pd
import altair as alt

# ===== Page Configuration =====
st.set_page_config(page_title="🎥 Movie Explorer", layout="centered")

# ===== Title and Instructions =====
st.title("🎬 Movie Explorer App")
st.markdown("Search for a movie and explore its ratings, genre, and more!")

# ===== User Inputs =====
api_key = st.text_input("Enter your OMDb API key:", type="password")
movie_title = st.text_input("Enter a movie title:", "Inception")

# ===== API Call Function =====
@st.cache_data
def fetch_movie_data(title, key):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# ===== Action Button =====
if st.button("Search Movie"):
    if not api_key:
        st.warning("Please enter a valid OMDb API key.")
    else:
        data = fetch_movie_data(movie_title, api_key)

        if "error" in data or data.get("Response") == "False":
            st.error(f"Movie not found or API error: {data.get('Error', 'Unknown error')}")
        else:
            # ===== Display Movie Info =====
            st.subheader(f"🎞️ {data['Title']} ({data['Year']})")
            st.image(data["Poster"])
            st.markdown(f"**Genre**: {data['Genre']}")
            st.markdown(f"**Director**: {data['Director']}")
            st.markdown(f"**Actors**: {data['Actors']}")
            st.markdown(f"**Plot**: {data['Plot']}")

            # ===== Ratings Table =====
            if data["Ratings"]:
                st.subheader("⭐ Ratings")
                ratings_df = pd.DataFrame(data["Ratings"])
                ratings_df.columns = ["Source", "Value"]
                st.dataframe(ratings_df)

                # ===== Visualization 1: Ratings Bar Chart =====
                st.subheader("📊 Ratings Comparison")
                chart = alt.Chart(ratings_df).mark_bar().encode(
                    x="Source",
                    y=alt.Y("Value", sort="-x"),
                    color=alt.Color("Source"),
                    tooltip=["Source", "Value"]
                ).properties(width=600)
                st.altair_chart(chart)

            # ===== Visualization 2: Genre Breakdown =====
            st.subheader("🎨 Genre Breakdown")
            genres = [g.strip() for g in data["Genre"].split(",")]
            genre_df = pd.DataFrame({"Genre": genres, "Count": [1] * len(genres)})

            pie_chart = alt.Chart(genre_df).mark_arc().encode(
                theta="Count",
                color="Genre",
                tooltip="Genre"
            )
            st.altair_chart(pie_chart)

            # ===== Expandable Full JSON =====
            with st.expander("🔍 See Full Raw JSON"):
                st.json(data)



