import streamlit as st 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth

#set up spotify credentials 
client_id="48d3561ba3804ea2a0b835b28681747f"
client_secret="c2577d5e7bb64a78b42980eca826abf0"
client_credentials_manager= SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp=spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_recommendations(track_name):
    #get Track URL 
    result=sp.search(q=track_name,type='track')
    track_uri=result['tracks']['items'][0]['uri']

    #get recommended tracks
    recommendations=sp.recommendations(seed_tracks=[track_uri])['tracks']
    return recommendations 

sp_oauth=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="48d3561ba3804ea2a0b835b28681747f",
                                               client_secret="c2577d5e7bb64a78b42980eca826abf0",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))
results=sp_oauth.current_user()
User_id=results['id']
st.set_page_config(page_title="Tell me a song",page_icon=" 🎶")
st.title("Music Recommendation System: 🎶")

track_name=st.text_input("Tell me a song you love")

titles=[]

if track_name:
    recommendation=get_recommendations(track_name)
    st.write("Songs I would recommend:")
    for track in recommendation:
        st.write(track['name'])
        st.image(track['album']['images'][0]['url'])
    st.subheader("Do you want to turn these songs into a playlist?")
    if st.button("Make Playlist"):
        inp=st.text_input("what do you want to name your playlist?")
        if inp:
            PLAYLIST_ID = sp_oauth.user_playlist_create(user=User_id,public=False,name=f"{inp}")['id']
            for track in recommendation:
                song_name=track['name']
                titles.append(song_name)
            st.write(titles)
            sp_oauth.user_playlist_add_tracks(playlist_id=PLAYLIST_ID,tracks=titles,user=User_id)
            st.write("Made a playlist for you! enjoy!!")
        


