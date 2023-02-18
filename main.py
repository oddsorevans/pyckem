from pprint import pprint
import nfl_request

dates = ['2022-09-30','2022-10-02','2022-10-03']
gameData = nfl_request.getGamesData(dates)
pprint(gameData)