%%writefile app.py
import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(new_df.iloc[i[0]].title)
    return recommended_movies

st.title('Movie Recommender System')

# Load the pickle files
try:
    with open('new_df.pkl', 'rb') as f:
        new_df = pickle.load(f)

    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    st.error("Error: pickle files not found. Please make sure 'new_df.pkl' and 'similarity.pkl' are in the same directory.")
    st.stop()


movie_list = new_df['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommendations = recommend(selected_movie)
    for i in recommendations:
        st.write(i)