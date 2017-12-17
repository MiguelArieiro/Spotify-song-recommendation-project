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
		self.followed=[]
		self.top=[]
		self.related=[]
		self.releases=[]


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
		artist_name=[]
		artist_id=[]
		album_name=[]
		album_id=[]
		genres=[]
		url=[]


		results=self.spotify.new_releases(country=None, limit=50, offset=0)
		
		for album in results['albums']['items']:
			temp_name=[]
			temp_id=[]

			for artist in album['artists']:
				temp_name.append(artist['name'])
				temp_name.append(artist['id'])

			artist_name.append(temp_name)
			artist_id.append(temp_id)
			album_name.append(album['name'])
			album_id.append(album['id'])
			url.append(album['external_urls'])
			self.spotify.album(album['id'])

		self.releases=[album_id, album_name, url, artist_id, artist_name]

	def __str__(self):
		string="»Top played artists:\n"
		temp="\n*Genres:\n"

		for i in range (len(self.top[0])):
			string += self.top[0][i] + ' - ' + self.top[1][i] + '\n'
			temp += self.top[2][i] + '\n'

		string += temp + "\n\n»Followed artists:\n"
		temp="\n*Genres:\n"

		for i in range (len(self.followed[0])):
			string += self.followed[0][i] + ' - ' + self.followed[1][i] + '\n'
			temp += self.followed[2][i] + '\n'

		string += temp + "\n\n»Related artists:\n"

		for i in range (len(self.related[0])):
			string += self.related[0][i] + ' - ' + self.related[1][i] + '; ' + str(self.related[2][i]) + '\n'
		
		string += temp + "\n\n»New releases:\n"

		for i in range (len(self.releases[0])):
			string += self.releases[0][i] + ' - ' + self.releases[1][i] + '\turl:  ' + self.releases[2][i] + '\n'
			for j in range (len(self.releases[3][i])):
				string += '\t-' + self.releases[3][i] + ' - ' + self.releases[4][i] + '\n'

		return string



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

	spotify.getTopArtists()
	spotify.getFollowed()
	spotify.getRelatedArtists()
	spotify.getReleases()

	print(spotify)

	
	