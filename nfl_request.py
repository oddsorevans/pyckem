from rapid_api_key import x_rapid_key, x_rapid_host

import requests
from pprint import pprint

def getGamesData(dates: list):
    url = "https://api-american-football.p.rapidapi.com/games"
    gameData = {}

    for date in dates:
        querystring = {"date":date,"league":"1"}
        headers = {
            "X-RapidAPI-Key": "e7dd9deb9amsh4edb5dd8a68beb9p13c86fjsn7b0d675d570f",
            "X-RapidAPI-Host": "api-american-football.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_response = response.json()
        for games in json_response['response']:
            home = games['teams']['home']['name']
            away = games['teams']['away']['name']
            versus = home + " vs. " + away
            gameData[versus] = {'home':home, 'away': away}
    return gameData

