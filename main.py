import nfl_request
import write_form

#insert the dates. Saturday and Monday night football you have to add 1 to the day due to an API error
dates = ['2022-09-30','2022-10-02','2022-10-04']
gameData = nfl_request.getGamesData(dates)

#insert week number, as well as the final game for the tierbreaker question
write_form.create_write_form(gameData, week= , final= )