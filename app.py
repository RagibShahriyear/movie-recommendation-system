import streamlit as st
import pickle
import requests

movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
api_key = YOUR_API_KEY


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{}?api_key={api_key}language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies_df[movies_df["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        # fetch poster
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies_df.iloc[i[0]].title)

    return recommended_movies, recommended_movie_posters


st.header('Movie Recommender System')

movies_list = movies_df['title'].values

selected_movie = st.selectbox(
    'Type or select a movie',
    movies_list)


if st.button('Show Recommendations'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movie_posters[4])





