import csv
import pygal
import operator
from pygal.style import CleanStyle, DefaultStyle
from collections import Counter

from HFA_home_goal_diff import HFA_goal_diff, HFA_goal_diff_season
from HFA_win_diff import HFA_home_wins, HFA_home_win_perc, HFA_home_win_perc_season
from HFA_by_team import HFA_team_results, HFA_team_goal_diff
from HFA_by_league import HFA_league_GD, HFA_league_results

#Leage options and filename
	# MLS - mls.csv
	# Premier League - england.csv
	# La Liga - spain.csv
	# Serie A - italy.csv
	# Budesliga - germany.csv
	# Ligue 1 - france.csv
	
filename = 'mls.csv'
HFA_home_win_perc_season(filename)



# MLS data included is 1996-2016 seasons incl. playoffs - 4995 games total



# I NEED TO APPLY CHANGES MADE TO HFA_BY_TEAM TO OTHER FUNCTIONS
