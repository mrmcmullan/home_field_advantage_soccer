import csv
import pygal
import operator
from pygal.style import CleanStyle, DefaultStyle
from collections import Counter

def HFA_league_GD():
	
	# Create list of filenames to loop through
	filenames = ['mls.csv', 'england.csv', 'spain.csv', 'italy.csv',
		'germany.csv', 'france.csv']
	
	# Initiate empty dicts to add league & goals scored pairs
	hg_per_league, ag_per_league = {}, {}
		
		
	# Loop though each league
	for filename in filenames:
		
		# Establish appropriate name for each league
		if filename == 'mls.csv':
			league_name = 'MLS'
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
		
		# Load data
		with open(filename) as f:
			data = csv.reader(f)
			header_row = next(data)
			
			# Establish goal and win variables as zero
			home_goals = 0
			away_goals = 0
		
			# Create empty dict to count games per season
			games_per_season = Counter()
			
			for row in data:
				# Normalize years included for each league
				# Start at 2000 since MLS shootout era ended then
				if int(row[1]) < 2000:
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
		
		# Fill dicts with league name and home & away goals / game
		hg_per_league[league_name] = home_goals_per_game
		ag_per_league[league_name] = away_goals_per_game
	
	# Use dicts to created sorted lists in order to plot
	leagues, sort_hg_per_league, sort_ag_per_league = [], [], []
	for league, goals in sorted(hg_per_league.items()):
		leagues.append(league)
		sort_hg_per_league.append(goals)
	for league, goals in sorted(ag_per_league.items()):
		sort_ag_per_league.append(goals)
	
	# Subtract home - away goals in order to visualize total GD	
	sort_gd = list(map(operator.sub, 
		sort_hg_per_league, sort_ag_per_league))
	
	# Plot
	league_gd = pygal.Bar()
	league_gd.title = 'Home and Away Goals Scored Per Game'
	league_gd.x_labels = leagues
	league_gd.add('Home Goals per Game', sort_hg_per_league)
	league_gd.add('Away Goals per Game', sort_ag_per_league)
	league_gd.add('Goal Difference per Gam', sort_gd)
	league_gd.render_in_browser()
		

def HFA_league_results():
	
	# Create list of filenames to loop through
	filenames = ['mls.csv', 'england.csv', 'spain.csv', 'italy.csv',
		'germany.csv', 'france.csv']
	
	# Initiate empty dicts to add league & goals scored pairs
	hw_perc_league, draw_perc_league, aw_perc_league = {}, {}, {}
	
	# Loop though each league
	for filename in filenames:
		
		# Establish appropriate name for each league
		if filename == 'mls.csv':
			league_name = 'MLS'
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
		
		# Load data
		with open(filename) as f:
			data = csv.reader(f)
			header_row = next(data)
			
			# Establish game result and number of games variables as zero
			total_hw, total_draws, total_aw, total_games = 0, 0, 0, 0
	
			
			for row in data:
				# Normalize years included for each league
				# Start at 2000 since MLS shootout era ended then
				if int(row[1]) < 2000:
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
					
		
		
		assert total_hw + total_draws + total_aw == total_games
		# Calculate percentages
		hw_perc = round((total_hw / total_games * 100), 2)
		draw_perc = round((total_draws / total_games * 100), 2)
		aw_perc = round((total_aw / total_games * 100), 2)
		
		hw_perc_league[league_name] = hw_perc
		draw_perc_league[league_name] = draw_perc
		aw_perc_league[league_name] = aw_perc
	
	# Use dicts to create sorted lists to plot
	sort_hw_perc_league, sort_draw_perc_league, sort_aw_perc_league = [], [], []
	leagues = []
	for league, wins in sorted(hw_perc_league.items()):
		leagues.append(league)
		sort_hw_perc_league.append(wins)
	for league, draws in sorted(draw_perc_league.items()):
		sort_draw_perc_league.append(draws)
	for league, wins in sorted(aw_perc_league.items()):
		sort_aw_perc_league.append(wins)
		
	# Plot result percentages for each league
	results = pygal.Bar()
	results.title = 'Average Win % for Various Leagues'
	results.x_labels = leagues
	results.add('Home Win %', sort_hw_perc_league)
	results.add('Draw %', sort_draw_perc_league)
	results.add('Away Win %', sort_aw_perc_league)
	results.render_in_browser()
	
	# Calculate average points per game earned at home vs away
	ppg_home, ppg_away = [], []
	for league in range(len(leagues)):
		ppg_home.append((sort_hw_perc_league[league] / 100 * 3) +
			(sort_draw_perc_league[league] / 100)) 
	ppg_home = [round(x, 2) for x in ppg_home]
	
	for league in range(len(leagues)):
		ppg_away.append((sort_aw_perc_league[league] / 100 * 3) +
			(sort_draw_perc_league[league] / 100))
	ppg_away = [round(x, 2) for x in ppg_away]
	
	# Plot ppg at home and away
	ppg = pygal.Bar(x_label_rotation=40)
	ppg.title = 'Various Leagues Average Points Per Game Home & Away'
	ppg.x_labels = leagues
	ppg.add('PPG at Home', ppg_home)
	ppg.add('PPG Away', ppg_away)
	ppg.render_in_browser()
		
