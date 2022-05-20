# opgg-scrape
Scrapes op.gg for wins/losses for up to 20 games played in the last 24 hours.

Dependencies:

  Requires Python 3 (Supported/Created With Python Versions 3.0 - 3.7 in Mind)

Python Packages:
- bs4
- lxml
- requests

Simply write get_recent_match_history(*league account name*) to get recent results as a Python dictionary.
 
Specifying Gamemode and Gamemode Results:
  - If you wish to exclude certain gamemodes from the result you may do so by specifying the list of gamemodes
  that you wish to keep track of by using the 'game_modes' keyword argument in get_recent_match_history.


  - By default, all results are returned when obtaining match history but you may specify to only include wins 
  (using 'wins') or losses (using 'losses') in the 'result' keyword argument in get_recent_match_history.
  The keyword argument 'result' is functionally case insentative (capitalization does not matter). 
 
League Accounts on Other Servers (Outside of North America): 
  - If the inputted account is not located on the North American server, you can specify the server by using the
  'region' keyword argument in get_recent_match_history. This keyword argument uses the abbreviation for each
  regions server and is functionally case insensitive (capitalization does not matter).

Not Showing Correct Results:
- Currently the program requires that the inputted league account be updated on op.gg beforehand. In future implementations I intend on
automating the profile updating proccess.
