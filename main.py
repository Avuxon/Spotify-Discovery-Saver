import json
import requests
from secrets import spotify_user_id, spotify_token, discover_weekly_id

class SaveSongs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""

    def find_songs(self):
        #loop thru playlist tracks & add them to a list

        print("Finding songs in discover weekly...")

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_weekly_id)

        response = requests.get(query,
        headers={"Content-type": "application/json", 
        "Authorization": "Bearer {}".format(spotify_token)})

        response_json = response.json()
        print(response)

        for i in response_json["items"]:
            self.tracks += i["track"]["uri"] + ","
        self.tracks = self.tracks[:-1]
        print(self.tracks)



a = SaveSongs()
a.find_songs()