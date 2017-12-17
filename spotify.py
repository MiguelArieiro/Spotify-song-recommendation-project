import spotipy
import sys
import os
import json
import pprint
import spotipy.oauth2 as oauth2
import spotipy.util as util

from operator import itemgetter #sorts lists


class Sensor:
	CLIENT_ID='50244e1334d342359b7bd26d72288c0c'
	CLIENT_SECRET='e45d6cf4ad5349cb9d39a9fa416f0824'
	REDIRECT_URI='https://localhost:8888/callback'

	def __init__ (self, username):
		self.username=User(username)
		scope='user-read-recently-played user-top-read user-follow-read playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private ugc-image-upload user-follow-modify user-follow-read'
		token = util.prompt_for_user_token(self.username.userID, scope,client_id=self.CLIENT_ID,client_secret=self.CLIENT_SECRET,redirect_uri=self.REDIRECT_URI)
		self.spotify=spotipy.Spotify(auth=token)


	def show_tracks(self, tracks):
		for i, item in enumerate(tracks['items']):
			track = item['track']
			print (" %d %32.32s %s" % (i, track['artists'][0]['name'],track['name']))


	def getFollowed(self):
		#os.system('cls')
		name=[]
		artist_id=[]
		genres=[]

		results = self.spotify.current_user_followed_artists()
		#pprint.pprint(results)

		counter=0
		while True:
			counter+=20
			for item in results['artists']['items']:
				artist_id.append(item['id'])
				name.append(item['name'])

				for genre in item['genres']:
					if genre not in genres:
						genres.append(genre);

				after_id=item['id']
			if len (results['artists']['items'])==0:
				break
			results = self.spotify.current_user_followed_artists(limit=20, after=after_id)
		
		self.followed=[artist_id, name, genres]
		

	def getTopArtists(self):
		#os.system('cls')
		name=[]
		artist_id=[]
		genres=[]

		results = self.spotify.current_user_top_artists()
		#pprint.pprint(results)
		
		for item in results['items']:	
			artist_id.append(item['id'])
			name.append(item['name'])		

			for genre in item['genres']:
				if genre not in genres:
					genres.append(genre);

			

		self.top=[artist_id, name, genres]

	def getRelatedArtists(self):
		#os.system('cls')
		name=[]
		artist_id=[]
		count=[]


		for artist in self.top[0]:
			results=self.spotify.artist_related_artists(artist)
			for item in results['artists']:
				if (item['id'] not in self.top[0]) and (item['id'] not in self.followed[0]):

					if (item['id'] not in artist_id):
						artist_id.append(item['id'])
						name.append(item['name'])
						count.append(1);
					else:
						count[artist_id.index(item['id'])]+=1;

		self.related=[artist_id, name, count]
			
	def getReleases(self):
		results=self.spotify.new_releases(country=None, limit=50, offset=0)
		pprint.pprint(results)


class Artist:

	def __init__ (self, name, id):
		self.name=name
		self.id=id

	def __str__(self):
		return (self.name)

	def __repr__(self):
		return (self.name)

	def __cmp__ (self, string):
		return cmp(self.name, string)

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

	spotify=Sensor(user.userID)
	spotify.getFollowed()

	spotify.getTopArtists()
	pprint.pprint(spotify.top)

	if 'My Chemical Romance' in spotify.top[1]:
		print ("this shit's kinda working")
	else:
		print("wtf am I doing with my life??????")

	spotify.getRelatedArtists()
	pprint.pprint(spotify.related)

	spotify.getReleases()
	