import spotipy
import sys
import os
import json
import pprint
import spotipy.oauth2 as oauth2
import spotipy.util as util



class Sensor:
    CLIENT_ID='50244e1334d342359b7bd26d72288c0c'
    CLIENT_SECRET='e45d6cf4ad5349cb9d39a9fa416f0824'
    REDIRECT_URI='https://localhost:8888/callback'

    def __init__ (self, username):
        self.username=username
        scope='user-read-recently-played user-top-read user-follow-read playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private ugc-image-upload user-follow-modify user-follow-read'
        token = util.prompt_for_user_token(username, scope,client_id=self.CLIENT_ID,client_secret=self.CLIENT_SECRET,redirect_uri=self.REDIRECT_URI)
        self.spotify=spotipy.Spotify(auth=token)


    def show_tracks(self, tracks):
        for i, item in enumerate(tracks['items']):
            track = item['track']
            print (" %d %32.32s %s" % (i, track['artists'][0]['name'],track['name']))


    def getFollowers(self):
        os.system('cls')
        
        results = self.spotify.current_user_followed_artists()
        #pprint.pprint(results)

        counter=0
        while True:
            counter+=20

            for item in results['artists']['items']:
                genres=''
                for genre in item['genres']:
                    genres+= genre+'; '
                print(item['name'] + ' - ' + genres)
                id=item['id']
            if len (results['artists']['items'])==0:
                break
            results = self.spotify.current_user_followed_artists(limit=20,after=id)
            
    #def getRelatedArtists(self):
        

    def getTopArtists(self):
        os.system('cls')
        results = self.spotify.current_user_top_artists()
        artists=[]
        genres=[]

        pprint.pprint(results)
        
        for item in results['items']:
            artists.append([item['name'],item['id']])

            #gets genres
            for genre in item['genres']:
                if genre not in genres:
                    genres.append(genre)

        #pprint.pprint(artists)
        #pprint.pprint(genres)

        r=[artists, genres]
        self.top=r

    def getRelatedArtists(self)
        related=[]
        for item in r[0]:
            results=self.spotify.get_related_artists()
            pprint.pprint(results)
            


class Artist:

    def __init__ (self, name):
        self.name=name

class User:

    def __init__ (self, userID):
        self.userID=userID

class Preferences:

    def __init__ (self, genres, value, spotifyID):
        self.type=genre
        self.value=value
        self.spotifyID=spotifyID


class Agente:
    def __init__ (self):
        x=1

class Lista:
    def __init__ (self, agent):
        x=1

if __name__ == '__main__':

	#user's username
    username='unpunished'
    user=User(username)

    spotify=Sensor(user.userID);
    pprint.pprint(spotify.getTopArtists())
    

