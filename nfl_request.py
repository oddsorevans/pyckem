#add rapidAPI keys. stored in external file.
from misc.rapid_api_key import x_rapid_key, x_rapid_host

import requests
import os

def getGamesData(dates: list):
    url = "https://api-american-football.p.rapidapi.com/games"
    gameData = {}
    rapidKey = x_rapid_key
    rapidHost = x_rapid_host

    for date in dates:
        querystring = {"date":date,"league":"1"}
        headers = {
            "X-RapidAPI-Key": rapidKey,
            "X-RapidAPI-Host": rapidHost
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_response = response.json()
        for games in json_response['response']:
            home = games['teams']['home']['name']
            away = games['teams']['away']['name']
            versus = home + " vs. " + away
            gameData[versus] = {'home':home, 'away': away}
    return gameData

