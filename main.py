import json
from wsgiref import headers
import requests
from secrets import spotify_user_id, discover_weekly_id #spotify_token
from datetime import date
from refresh import Refresh

class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = "" #spotify_token
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""

    def find_songs(self):
        #loop thru playlist tracks & add them to a list

        print("Finding songs in discover weekly...")

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_weekly_id)

        response = requests.get(query,
        headers={"Content-type": "application/json", 
        "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()
        #print(response)

        for i in response_json["items"]:
            self.tracks += i["track"]["uri"] + ","
        self.tracks = self.tracks[:-1]

        self.add_to_playlist()

    def create_playlist(self):
        #Create a new playlist so you can save discovery songs for longer than a week
        print("Attempting to create playlist...")
        today = date.today()
        todayformatted = today.strftime("%m/%d/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        request_body = json.dumps({
            "name": todayformatted + " Discover Weekly",
            "description": "Discover Weekly recovered from being deleted every week via a simple python script", 
            "public": True
        })

        response = requests.post(query, data=request_body, headers={
            "Content-type": "application/json", 
            "Authorization": "Bearer {}".format(self.spotify_token)
        })

        response_json = response.json()
        return response_json["id"]
        #print(response)

    def add_to_playlist(self):
        # add all songs to new playlist
        print("Adding songs...")
        self.new_playlist_id = self.create_playlist()
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.new_playlist_id, self.tracks)
        response = requests.post(query, headers = {
            "Content-type": "application/json", 
            "Authorization": "Bearer {}".format(self.spotify_token) 
        })
        #print(response.json)

    def call_refresh(self):
        print("Refreshing Token")
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()
        self.find_songs()

a = SaveSongs()
a.call_refresh()