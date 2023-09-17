import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url='https://api.themoviedb.org/3/movie/{}?api_key=aedfbcee9d5c9c6cffc39c46ca0f4a07&language=en-US'.format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500" + poster_path
    return full_path

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    
    movies_list=sorted(list(enumerate(similarity[movie_index])),reverse=True,key=lambda x:x[1])
    recom_movie=[]
    recom_movie_posters=[]

    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recom_movie.append(movies.iloc[i[0]].title)
        recom_movie_posters.append(fetch_poster(movie_id))
    return recom_movie,recom_movie_posters

st.title('Movie Recomender System')

movies_dict=pickle.load(open('movies.pkl','rb'))
movies=pd.DataFrame(movies_dict)


movie_list=movies['title'].values

option=st.selectbox(
    'Which movie you want to see',
    movies['title'].values
)

similarity=pickle.load(open('similarity.pkl','rb'))


if st.button('Recommend'):
    names,posters=recommend(option)
    for i in names:
        st.write(i)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
 
 

    