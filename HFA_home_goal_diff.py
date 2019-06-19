import csv
import pygal
import operator
import pandas as pd
from pygal.style import CleanStyle, DefaultStyle
from collections import Counter

def HFA_goal_diff(filename):
	if filename == 'mls.csv':
		league_name = 'MLS'
		season_label = '2000-2016'
		save_f = 'mls_goal_diff.svg'
	elif filename == 'england.csv':
		league_name = 'English Premier League'
	elif filename == 'spain.csv':
		league_name = 'La Liga'
	elif filename == 'italy.csv':
		league_name = 'Serie A'
	elif filename == 'france.csv':
		league_name = 'Ligue 1'
	elif filename == 'germany.csv':
		league_name = 'Bundesliga'
		
	# Import data
	# MLS data included is 1996-2016 seasons incl. playoffs - 4995 games total
	with open(filename) as f:
		data = csv.reader(f)
		header_row = next(data)
		
		# Establish goal and win variables as zero
		home_goals = 0
		away_goals = 0
	
		# Create empty dict to count games per season
		games_per_season = Counter()
		
		for row in data:
			# Remove mls shoutout era results
			if filename == 'mls.csv':
				if int(row[1]) < 2000:
					continue
					
			# Remove lower english divisions
			# Remove era prior to PL formation
			if filename == 'england.csv':
				if row[7] != '1':
					continue
				if int(row[1]) < 1992:
					continue
		
			# Calculate total home & away goals for all years
			home_goals += int(row[5])
			away_goals += int(row[6])
			
			# Count games per season
			games_per_season[row[1]] += 1
			
	# TOTAL HOME FIELD ADVANTAGE OVER ALL SEASONS
	# Calculate home & away goals per game
	total_games = 0
	for games in games_per_season.values():
		total_games += games
	home_goals_per_game = round(home_goals / total_games, 2)
	away_goals_per_game = round(away_goals / total_games, 2)
	
	# Plot MLS data all seasons per game
	goals = pygal.Bar()
	goals.title = league_name + ' Home vs Away Goals Per Game for Seasons ' + season_label
	goals.add('Home Goals', home_goals_per_game)
	goals.add('Away Goals', away_goals_per_game)
	goals.render_to_file(save_f)
	

def HFA_goal_diff_season(filename):
	if filename == 'mls.csv':
		league_name = 'MLS'
		season_label = '2000-2016'
		save_f = 'mls_goal_diff_season.svg'
	elif filename == 'england.csv':
		league_name = 'English Premier League'	
	elif filename == 'spain.csv':
		league_name = 'La Liga'
	elif filename == 'italy.csv':
		league_name = 'Serie A'
	elif filename == 'france.csv':
		league_name = 'Ligue 1'
	elif filename == 'germany.csv':
		league_name = 'Bundesliga'
	
	# Import data
	# MLS data included is 1996-2016 seasons incl. playoffs - 4995 games total
	with open(filename) as f:
		data = csv.reader(f)
		header_row = next(data)
	
		# Create empty dicts to count home & away goals, games per season
		# and total goals for each team
		season_hg = Counter()
		season_ag = Counter()
		games_per_season = Counter()
		
		for row in data:
			# Remove mls shoutout era results
			if filename == 'mls.csv':
				if int(row[1]) < 2000:
					continue
				
			# Remove lower english divisions
			# Remove era prior to PL formation
			if filename == 'england.csv':
				if row[7] != '1':
					continue
				if int(row[1]) < 1992:
					continue
			
			# Count number of home & away goals per season
			season_hg[row[1]] += int(row[5])
			season_ag[row[1]] += int(row[6])
			
			# Count games per season
			games_per_season[row[1]] += 1
	
	# HOME FIELD ADVANTAGE (GOAL DIFFERENCE) PER SEASON
	# Convert dictionaries into sorted lists in order to plot
	seasons = []
	hg_per_season, ag_per_season, gd_per_season = [], [], []
	number_of_games = []
	
	# Convert seasons/home goals to sorted list
	for season, goals in sorted(season_hg.items()):
		# Create list of sorted season years
		seasons.append(season)
		hg_per_season.append(goals)
		
	# Convert seasons/away goals to sorted list
	for season, goals in sorted(season_ag.items()):
		ag_per_season.append(goals)
	
	# Convert season/number of games to sorted list	
	for season, games in sorted(games_per_season.items()):
		number_of_games.append(games)
			
	# Calculate goal difference by home goals - away goals per season	
	gd_per_season = list(map(operator.sub, hg_per_season, ag_per_season))
	
	# Calculate season average home team goal difference per game
	gd_per_game_per_season = list(map(operator.truediv,
		gd_per_season, number_of_games))
	gd_per_game_per_season = [round(x, 2) for x in gd_per_game_per_season]
	
	# Calculate 21 year average home goal difference per game
	average = [sum(gd_per_game_per_season) / len(gd_per_game_per_season)
		for x in range(0, len(gd_per_game_per_season))]
	average = [round(x, 2) for x in average]
		
	# Plot data per game per season
	lc = pygal.Line(x_label_rotation = 20)
	lc.title = league_name + ' Home Goal Difference Per Game for Seasons ' + season_label
	lc.x_labels = map(str, seasons)
	lc.add('Goal Difference', gd_per_game_per_season)
	#lc.add('Average', average)
	lc.render_to_file(save_f)
	
	
