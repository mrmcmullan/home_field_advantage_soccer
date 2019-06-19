import csv
import pygal
import operator
from pygal.style import CleanStyle, DefaultStyle
from collections import Counter

def HFA_home_wins(filename):
	if filename == 'mls.csv':
		league_name = 'MLS'
		season_label = '2000-2016'
		save_f = 'mls_home_wins.svg'
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
	with open(filename) as f:
		data = csv.reader(f)
		header_row = next(data)
			
		# Establish game result variables as zero
		total_hw, total_draws, total_aw = 0, 0, 0
		
		for row in data:
			# Remove mls post shoutout era results
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
			
			# Count the number of home wins, draws, away wins
			# Also count per team
			if row[5] > row[6]:
				total_hw +=1
				
						
			elif row[5] == row[6]:
				total_draws += 1
				
			else:
				total_aw += 1
				
	
	# HOW OFTEN DO TEAMS WIN HOME VS AWAY??
	# Confirm have proper number of games
	
	# Plot MLS home wins, draws, and away wins
	wins = pygal.Bar(print_values=True, style=DefaultStyle(
	                  value_font_family='googlefont:Raleway',
	                  value_font_size=30,
	                  value_colors=('white','white','white')))
	wins.title = league_name + ' Total Home Wins, Draws, and Away Wins (in %) for Seasons ' + season_label
	wins.add('Home Wins', total_hw)
	wins.add('Draws', total_draws)
	wins.add('Away Wins', total_aw)
	wins.render_in_file(save_f)



def HFA_home_win_perc(filename):
	if filename == 'mls.csv':
		league_name = 'MLS'
		season_label = '2000-2016'
		save_f = 'mls_home_win_perc.svg'
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
	with open(filename) as f:
		data = csv.reader(f)
		header_row = next(data)
			
		# Establish game result and number of games variables as zero
		total_hw, total_draws, total_aw, total_games = 0, 0, 0, 0

		
		for row in data:
			# Remove post shoutout era results
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
							
			# Count games per season
			total_games += 1
			
			# Count the number of home wins, draws, away wins
			# Also count per team
			if row[5] > row[6]:
				total_hw +=1
										
			elif row[5] == row[6]:
				total_draws += 1
				
			else:
				total_aw += 1
				
	
	# Plot home win %, draw %, and away win %
	assert total_hw + total_draws + total_aw == total_games
	# Calculate percentages
	hw_perc = round((total_hw / total_games * 100), 2)
	draw_perc = round((total_draws / total_games * 100), 2)
	aw_perc = round((total_aw / total_games * 100), 2)
	
	#Plot
	wins = pygal.Bar(print_values=True, style=DefaultStyle(
	                  value_font_family='googlefont:Raleway',
	                  value_font_size=30,
	                  value_colors=('white','white','white')))
	wins.title = league_name + ' Results (in %) for Seasons ' + season_label
	wins.add('Home Win %', hw_perc)
	wins.add('Draw %', draw_perc)
	wins.add('Away Win %', aw_perc)
	wins.render_to_file(save_f)
	
	
def HFA_home_win_perc_season(filename):
	if filename == 'mls.csv':
		league_name = 'MLS'
		season_label = '2000-2016'
		save_f = 'mls_home_win_perc_season.svg'
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
	with open(filename) as f:
		data = csv.reader(f)
		header_row = next(data)
			
		# Establish goal and win variables as zero
		total_hw, total_draws, total_aw, total_games = 0, 0, 0, 0
		
		# Create empty dicts to count home & away goals, games per season
		# and total goals for each team
		games_per_season = Counter()
		home_wins = Counter()
		draws = Counter()
		away_wins = Counter()
		
		for row in data:
			# Remove post shoutout era results
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
			
			# Count games per season
			games_per_season[row[1]] += 1
			total_games += 1			
			
			# Count the number of home wins, draws, away wins
			# Also count per team
			if row[5] > row[6]:
				home_wins[row[1]] += 1				
						
			elif row[5] == row[6]:
				draws[row[1]] += 1
				
			else:
				away_wins[row[1]] += 1
					
	
	# Convert season/number of games to sorted list	
	seasons, number_of_games = [], []
	for season, games in sorted(games_per_season.items()):
		number_of_games.append(games)
		seasons.append(season)
	
	# Plot home win %, draw %, and away win % per season
	# Divide win totals per season by number of games per season
	hw_season, draws_season, aw_season = [], [], []
	for season, hws in sorted(home_wins.items()):
		hw_season.append(hws)
	hw_season_perc = list(map(operator.truediv,
		hw_season, number_of_games))
	hw_season_perc = [round(x * 100, 2) for x in hw_season_perc]
	for season, draw in sorted(draws.items()):
		draws_season.append(draw)
	draws_season_perc = list(map(operator.truediv,
		draws_season, number_of_games))	
	draws_season_perc = [round(x * 100, 2) for x in draws_season_perc]
	for season, aws in sorted(away_wins.items()):
		aw_season.append(aws)
	aw_season_perc = list(map(operator.truediv,
		aw_season, number_of_games))
	aw_season_perc = [round(x * 100, 2) for x in aw_season_perc]
		
	# Plot
	wins_season = pygal.Bar(showlegend=False)
	wins_season.title = league_name + ' Results During (in %) for Seasons ' + season_label
	wins_season.x_labels = seasons
	wins_season.add('Home Win %', hw_season_perc)
	wins_season.add('Draw %', draws_season_perc)
	wins_season.add('Away Win %', aw_season_perc)
	wins_season.render_to_file(save_f)
		
	
