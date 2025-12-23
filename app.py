import streamlit as st
import pickle
import pandas as pd
import requests

# ------------------ Fetch Poster using OMDb ------------------
def fetch_poster(movie_title):
    url = "https://www.omdbapi.com/"
    params = {
        "t": movie_title,
        "apikey": "230df4e"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        poster = data.get("Poster")
        if poster and poster != "N/A":
            return poster
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Error"

# ------------------ Recommendation Function ------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_movie_posters.append(fetch_poster(title))

    return recommended_movies, recommended_movie_posters

# ------------------ Load Data ------------------
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------ Streamlit UI ------------------
st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Which movie do you want?',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
