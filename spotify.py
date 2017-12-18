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
		self.followed=[[],[],[]]
		self.top=[[],[],[]]
		self.related=[[],[],[]]
		self.releases=[[],[],[],[],[]]


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

		name=[x for _, x in sorted(zip(count,name), key=lambda pair: pair[0], reverse=True)]
		artist_id=[x for _, x in sorted(zip(count,artist_id), key=lambda pair: pair[0], reverse=True)]
		count=sorted(count, reverse=True)

		name=name[:20]
		artist_id=artist_id[:20]
		count=count[:20]
		self.related=[artist_id, name, count]
			
	def getReleases(self):
		artist_name=[]
		artist_id=[]
		album_name=[]
		album_id=[]
		genres=[]
		url=[]
		points=[]


		results=self.spotify.new_releases(country=None, limit=50, offset=0)
		
		for album in results['albums']['items']:
			temp_name=[]
			temp_id=[]
			temp_genres=[]

			for artist in album['artists']:
				temp_name.append(artist['name'])
				temp_id.append(artist['id'])
				temp_genres=self.spotify.artist(artist['id'])['genres']

			artist_name.append(temp_name)
			artist_id.append(temp_id)
			genres.append(temp_genres)

			album_name.append(album['name'])
			album_id.append(album['id'])
			url.append(album['external_urls']['spotify'])
			points.append(0)


		self.releases=[album_id, album_name, url, artist_id, artist_name, genres, points]

	def getInfo(self):
		self.getTopArtists()
		self.getFollowed()
		self.getRelatedArtists()
		self.getReleases()

	def __str__(self):
		string="»Top played artists:\n"
		temp="*Genres:\n"

		for i in range (len(self.top[0])):
			string += self.top[1][i] + '\n'
			temp += self.top[2][i] + '\n'

		string += temp + "\n\n»Followed artists:\n"
		temp="*Genres:\n"

		for i in range (len(self.followed[0])):
			string +=  self.followed[1][i] + '\n'
			temp += self.followed[2][i] + '\n'

		string += temp + "\n\n»Related artists:\n"

		for i in range (len(self.related[0])):
			string += self.related[1][i] + '; ' + str(self.related[2][i]) + '\n'
		
		string += "\n\n»New releases:\n"

		for i in range (len(self.releases[0])):
			string +=self.releases[1][i] + "\turl:  " + self.releases[2][i] + '\n'
			for j in range (len(self.releases[3][i])):
				string += '\t-' + self.releases[4][i][j] + '\n'

		return string


class User:

	def __init__ (self, userID):
		self.userID=userID

class Preferences:

	def __init__ (self, genres, value, spotifyID):
		self.type=genre
		self.value=value
		self.spotifyID=spotifyID


class Agent:
	def __init__ (self, username):
		self.suggestions=[[],[],[],[],[],[],[]]
		self.spotify=Sensor(username)

	def startup(self):
		self.suggestions=[self.spotify.releases[0][:], self.spotify.releases[1][:], self.spotify.releases[2], self.spotify.releases[3], self.spotify.releases[4], self.spotify.releases[5], self.spotify.releases[6]]

	def sortSuggestions(self):

		index=[]

		for i in range (len(self.suggestions[6])):
			if self.suggestions[6][i]==0:
				index.append(i)

		for i in reversed (index):
			self.suggestions[0].pop(i)
			self.suggestions[1].pop(i)
			self.suggestions[2].pop(i)
			self.suggestions[3].pop(i)
			self.suggestions[4].pop(i)
			self.suggestions[5].pop(i)
			self.suggestions[6].pop(i)

		self.suggestions[0]=[x for _, x in sorted(zip(self.suggestions[6],self.suggestions[0]), key=lambda pair: pair[0], reverse=True)]
		self.suggestions[1]=[x for _, x in sorted(zip(self.suggestions[6],self.suggestions[1]), key=lambda pair: pair[0], reverse=True)]
		self.suggestions[2]=[x for _, x in sorted(zip(self.suggestions[6],self.suggestions[2]), key=lambda pair: pair[0], reverse=True)]
		self.suggestions[3]=[x for _, x in sorted(zip(self.suggestions[6],self.suggestions[3]), key=lambda pair: pair[0], reverse=True)]
		self.suggestions[4]=[x for _, x in sorted(zip(self.suggestions[6],self.suggestions[4]), key=lambda pair: pair[0], reverse=True)]
		self.suggestions[5]=[x for _, x in sorted(zip(self.suggestions[6],self.suggestions[5]), key=lambda pair: pair[0], reverse=True)]
		self.suggestions[6]=sorted(self.suggestions[6], reverse=True)


	def filterByTop (self):
		for i in range (len(self.spotify.releases[0])):
			for artist_id in self.spotify.releases[3][i]:
				if artist_id in self.spotify.top[0]:
					self.suggestions[6][i]+=75

	def filterByFollowed (self):
		for i in range (len(self.spotify.releases[0])):
			for artist_id in self.spotify.releases[3][i]:
				if (artist_id in self.spotify.followed[0]) and (artist_id not in self.spotify.top[0]):
					self.suggestions[6][i]+=50

	def filterByRelatedArtists (self):
		for artist_id in self.spotify.related[0]:
			for i in range (len(self.spotify.releases[0])):
				if artist_id in self.spotify.releases[3][i]:
					self.suggestions[6][i]+=25

	def filterByGenre (self):
		for i in range (len(self.spotify.releases[0])):

			for genre in self.spotify.releases[5][i]:
				if genre in self.spotify.top[2]:
					self.suggestions[6][i]+=5
				elif genre in self.spotify.followed[2]:
					self.suggestions[6][i]+=3
				



	def filter(self):
		self.spotify.getInfo()
		#print(self.spotify)
		self.startup()

		self.filterByTop()
		self.filterByFollowed()
		self.filterByRelatedArtists()
		self.filterByGenre()

		self.sortSuggestions()

		print(self)

	def __str__ (self):
		string = "\n\n»Suggested albums:\n"

		for i in range (len(self.suggestions[0])):
			string += self.suggestions[1][i] + "\turl:  " + self.suggestions[2][i] + '\tpoints: ' + str(self.suggestions[6][i]) + '\n'
			for j in range (len(self.suggestions[3][i])):
				string += '\t-' + self.suggestions[4][i][j] + '\n'

		return string


class Lista:
	def __init__ (self, agent):
		return

if __name__ == '__main__':
	os.system('cls')
	#user's username
	username=input("Username:")
	os.system('cls')
	user=User(username)
	agent=Agent(user.userID)
	agent.filter()

	#print(agent.spotify)

	
	