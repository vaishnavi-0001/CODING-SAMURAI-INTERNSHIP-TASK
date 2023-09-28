import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    base_url = "https://image.tmdb.org/t/p/original"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=0093872f0e579322af1ea3be4bccdc2d&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')  # Use .get() to handle missing key gracefully
    if poster_path:
        full_path = f"{base_url}{poster_path}"
    else:
        # Provide a default poster URL or handle the error as needed
        full_path = "default.jpg"
    return full_path


# Load movie data and similarity matrix
movies = pickle.load(open("movies_list.pk1", 'rb'))
similarity = pickle.load(open("similarity.pk1", 'rb'))
movies_list = movies['original_title'].values

st.header("Movies Recommendation System")

# Create a dropdown
selected_movie = st.selectbox("Select a movie: ", movies_list)

def recommend(movie):
    index = movies[movies['original_title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]]['id']  # Replace 'YOUR_COLUMN_NAME' with the actual column name for movie ID
        recommend_movie.append(movies.iloc[i[0]].original_title)
        recommend_poster.append(fetch_poster(movie_id))
    
    return recommend_movie, recommend_poster

if st.button("Show Recommendations"):
    movie_name, movie_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])

