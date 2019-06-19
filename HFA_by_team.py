import csv
import pygal
import operator
from pygal.style import CleanStyle, DefaultStyle
from collections import Counter

def HFA_team_results(filename):
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
		
	# Import data
	with open(filename) as f:
		data = csv.reader(f)
		header_row = next(data)
			
		# Establish goal and win variables as zero
		total_hw, total_draws, total_aw = 0, 0, 0
		
		# Create empty dicts to count home & away goals, games per season
		teams_home_wins, teams_home_draws, teams_home_loss = Counter(),	Counter(), Counter()
		teams_away_wins, teams_away_draws, teams_away_loss = Counter(),	Counter(), Counter()
		home_games_per_team, away_games_per_team = Counter(), Counter()
		
				
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
					
			# Only include more modern seasons?
			#if int(row[1]) < 1952:
			#	continue
			
			#Count games per team
			home_games_per_team[row[2]] += 1
			away_games_per_team[row[3]] += 1
			
			
			# Count the number of home wins, draws, away wins
			# Also count per team
			if row[5] > row[6]:				
				teams_home_wins[row[2]] += 1
				teams_away_loss[row[3]] += 1
						
			elif int(row[5]) == int(row[6]):				
				teams_home_draws[row[2]] += 1
				teams_away_draws[row[3]] += 1
				
			elif row[5] < row[6]:				
				teams_home_loss[row[2]] += 1
				teams_away_wins[row[3]] += 1
	
	print(len(home_games_per_team))
	# Delete teams who didn't play 2 seasons worth of home games
	teams_delete = []
	min_games = 0
	# for team, games in home_games_per_team.items():
		# if filename == 'mls.csv':
			# if games < 34:
				# teams_delete.append(team)
	
	while (len(home_games_per_team) - len(teams_delete)) > 20:
		for team, games in home_games_per_team.items():
			if games < min_games:
				if team not in teams_delete:
					teams_delete.append(team)
		min_games += 1
			
			
	print(len(teams_delete))
	for team in teams_delete:
		del home_games_per_team[team]
		del away_games_per_team[team]
		del teams_home_wins[team]
		del teams_away_loss[team]
		del teams_home_draws[team]
		del teams_away_draws[team]
		del teams_home_loss[team]
		del teams_away_wins[team]
	
	# DOES ANY TEAM HISTORICALLY HAVE BETTER HOME FIELD ADVANTAGE??
	# Calculate and plot win, draw, loss% for each team at home
	
	# Initiate empty list to store sorted data
	sort_teams, sort_team_hw, sort_team_home_draws, sort_team_hl = [], [], [], []
	sort_team_aw, sort_team_away_draws, sort_team_al = [], [], []
	sort_home_games_team, sort_away_games_team = [], []
	
	# DOES NYCFC ENJOY GREATER HFA B/C YANKEE STADIUM??
	# Added NYCFC's 2017 and 2018 seasons for mls
	
	# Create list with total number of games home and away sorted by team
	for team, games in sorted(home_games_per_team.items()):
		sort_teams.append(team)
		sort_home_games_team.append(games)
	if filename == 'mls.csv':
		sort_home_games_team[11] += 17
		sort_home_games_team[11] += 17
	print(len(sort_teams))
	
	for team, games in sorted(away_games_per_team.items()):
		sort_away_games_team.append(games)
	if filename == 'mls.csv':
		sort_away_games_team[11] += 17
		sort_away_games_team[11] += 17
		
	# Solve issue that occurs when team has no stat in a certain category
	# Ex - No home wins
	for team_name in sort_teams:
		if team_name not in teams_home_wins.keys():
			teams_home_wins[team_name] = 0
		elif team_name not in teams_away_loss.keys():
			teams_away_loss[team_name] = 0
		elif team_name not in teams_home_draws.keys():
			teams_home_draws[team_name] = 0	
		elif team_name not in teams_away_draws.keys():
			teams_away_draws[team_name] = 0
		elif team_name not in teams_home_loss.keys():
			teams_home_loss[team_name] = 0
		elif team_name not in teams_away_wins.keys():
			teams_away_wins[team_name] = 0
			
	
	#Create list with total home and away wins sorted by team
	for team, wins in sorted(teams_home_wins.items()):
		sort_team_hw.append(wins)
	if filename == 'mls.csv':
		sort_team_hw[11] += 10
		sort_team_hw[11] += 12
	
	for team, wins in sorted(teams_away_wins.items()):
		sort_team_aw.append(wins)
	if filename == 'mls.csv':
		sort_team_aw[11] += 6
		sort_team_aw[11] += 4
		
	# Calculate home and away win percent by team
	hw_team_perc = list(map(operator.truediv,
		sort_team_hw, sort_home_games_team))
	hw_team_perc = [round(x * 100, 2) for x in hw_team_perc]
	
	aw_team_perc = list(map(operator.truediv,
		sort_team_aw, sort_away_games_team))
	aw_team_perc = [round(x * 100, 2) for x in aw_team_perc]
	print(aw_team_perc)
	
	# Calculate home and away draw percent by team
	for team, draws in sorted(teams_home_draws.items()):
		sort_team_home_draws.append(draws)
	if filename == 'mls.csv':
		sort_team_home_draws[11] += 5
		sort_team_home_draws[11] += 4
	
	for team, draws in sorted(teams_away_draws.items()):
		sort_team_away_draws.append(draws)
	if filename == 'mls.csv':
		sort_team_away_draws[11] += 4
		sort_team_away_draws[11] += 4
	
	home_draw_team_perc = list(map(operator.truediv,
		sort_team_home_draws, sort_home_games_team))
	home_draw_team_perc = [round(x * 100, 2) for x in home_draw_team_perc]
	
	away_draw_team_perc = list(map(operator.truediv,
		sort_team_away_draws, sort_away_games_team))
	away_draw_team_perc = [round(x * 100, 2) for x in away_draw_team_perc]
	
	
	# Calculate home and away loss percent by team
	for team, losses in sorted(teams_home_loss.items()):
		sort_team_hl.append(losses)
	if filename == 'mls.csv':
		sort_team_hl[11] += 2
		sort_team_hl[11] += 1
	
	for team, losses in sorted(teams_away_loss.items()):
		sort_team_al.append(losses)
	if filename == 'mls.csv':
		sort_team_al[11] +=	7
		sort_team_al[11] += 9
	
	hl_team_perc = list(map(operator.truediv,
		sort_team_hl, sort_home_games_team))
	hl_team_perc = [round(x * 100, 2) for x in hl_team_perc]
	
	al_team_perc = list(map(operator.truediv,
		sort_team_al, sort_away_games_team))
	al_team_perc = [round(x * 100, 2) for x in al_team_perc]
	
	assert len(sort_teams) == len(sort_team_hw)
	assert len(sort_teams) == len(sort_team_hl)
	assert len(sort_teams) == len(away_draw_team_perc)
	
	# Plot average results at home per team
	home_results = pygal.Bar(x_label_rotation=40)
	home_results.title = league_name + ' Teams Average Win, Draw, & Loss % at Home'
	home_results.x_labels = sort_teams
	home_results.add('Home Win %', hw_team_perc)
	home_results.add('Draw %', home_draw_team_perc)
	home_results.add('Home Loss %', hl_team_perc)
	home_results.render_in_browser()
	
	# Plot average results away per team
	away_results = pygal.Bar(x_label_rotation=40)
	away_results.title = league_name + ' Teams Average Win, Draw, & Loss % Away'
	away_results.x_labels = sort_teams
	away_results.add('Away Win %', aw_team_perc)
	away_results.add('Away Draw %', away_draw_team_perc)
	away_results.add('Away Loss %', al_team_perc)
	away_results.render()
	
	# Calculate average points per game earned at home vs away
	ppg_home, ppg_away = [], []
	for team in range(len(sort_teams)):
		ppg_home.append((hw_team_perc[team] / 100 * 3) +
			(home_draw_team_perc[team] / 100)) 
	ppg_home = [round(x, 2) for x in ppg_home]
	
	for team in range(len(sort_teams)):
		ppg_away.append((aw_team_perc[team] / 100 * 3) +
			(away_draw_team_perc[team] / 100))
	ppg_away = [round(x, 2) for x in ppg_away]
	
	# Plot ppg at home and away
	ppg = pygal.Bar(x_label_rotation=40)
	ppg.title = league_name + ' Teams Average Points Per Game Home & Away'
	ppg.x_labels = sort_teams
	ppg.add('PPG at Home', ppg_home)
	ppg.add('PPG Away', ppg_away)
	ppg.render_in_browser()
	
	# Plot ppg difference home & away
	ppg_diff = list(map(operator.sub, 
		ppg_home, ppg_away))
	
	ppg = pygal.Bar(x_label_rotation=40)
	ppg.title = league_name + ' Teams Difference Between PPG Home & Away'
	ppg.x_labels = sort_teams
	ppg.add('Difference Between Average PPG Home & Away', ppg_diff)
	ppg.render() 

	


def HFA_team_goal_diff(filename):
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
			
	# Import data
	with open(filename) as f:
		data = csv.reader(f)
		header_row = next(data)
		# Initiate dicts for home and away goals scored FOR per team
		# Initiate dicts for home and away goals ALLOWED per team
		# Initiate dicts for home and away games per team
		teams_hg_scored, teams_ag_scored = Counter(), Counter()
		teams_hg_allowed, teams_ag_allowed = Counter(), Counter()
		home_games_per_team, away_games_per_team = Counter(), Counter()
		
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
			
			#Count home and away games per team
			home_games_per_team[row[2]] += 1
			away_games_per_team[row[3]] += 1
		
			# Count the number of home and away goals SCORED per team
			teams_hg_scored[row[2]] +=int(row[5])
			teams_ag_scored[row[3]] +=int(row[6])
			
			# Count the number of home and away goals ALLOWED per team
			teams_hg_allowed[row[2]] += int(row[6])
			teams_ag_allowed[row[3]] += int(row[5])
			
			
	# Delete teams who didn't play 2 seasons worth of home games
	teams_delete = []
	for team, games in home_games_per_team.items():
		if filename == 'mls.csv':
			if games < 34:
				teams_delete.append(team)
		else:
			if games < 200:
				teams_delete.append(team)
	
	for team in teams_delete:
		del home_games_per_team[team]
		del away_games_per_team[team]
		del teams_home_wins[team]
		del teams_away_loss[team]
		del teams_home_draws[team]
		del teams_away_draws[team]
		del teams_home_loss[team]
		del teams_away_wins[team]
	
	
	
	# WHICH TEAM HAS THE BIGGEST HISTORICAL DIFF B/W HOME & AWAY GOAL DIFF
	# IS IT NYCFC?
	
	# Create sorted list of teams & sorted list of number of games played
	sort_teams, sort_home_games_team, sort_away_games_team = [], [], []
	sort_teams_hg_scored, sort_teams_hg_allowed = [], []
	sort_teams_ag_scored, sort_teams_ag_allowed = [], []

	for team, games in sorted(home_games_per_team.items()):
		sort_teams.append(team)
		sort_home_games_team.append(games)
	if filename == 'mls.csv':
		sort_home_games_team[11] += 18
		sort_home_games_team[11] += 19
	
	for team, games in sorted(away_games_per_team.items()):
		sort_away_games_team.append(games)
	if filename == 'mls.csv':
		sort_away_games_team[11] += 18
		sort_away_games_team[11] += 18
		
	# Create sorted lists of goals scored for and goals allowed at home
	for team, home_goals in sorted(teams_hg_scored.items()):
		sort_teams_hg_scored.append(home_goals)
	if filename == 'mls.csv':
		sort_teams_hg_scored[11]  += 35
		sort_teams_hg_scored[11]  += 39
		
	for team, home_allowed in sorted(teams_hg_allowed.items()):
		sort_teams_hg_allowed.append(home_allowed)
	if filename == 'mls.csv':
		sort_teams_hg_allowed[11]  += 20
		sort_teams_hg_allowed[11]  += 12

	# Create sorted lists of goals scored and allowed away
	for team, away_goals in sorted(teams_ag_scored.items()):
		sort_teams_ag_scored.append(away_goals)
	if filename == 'mls.csv':
		sort_teams_ag_scored[11] += 24
		sort_teams_ag_scored[11] += 24
		
	for team, away_allowed in sorted(teams_ag_allowed.items()):
		sort_teams_ag_allowed.append(away_allowed)
	if filename == 'mls.csv':
		sort_teams_ag_allowed[11]  += 27
		sort_teams_ag_allowed[11]  += 38

	# Divide by number of games to get average goal diff home & away
	hg_per_game = list(map(operator.truediv,
		sort_teams_hg_scored, sort_home_games_team))
	hg_per_game = [round(x, 2) for x in hg_per_game]
		
	ha_per_game = list(map(operator.truediv,
		sort_teams_hg_allowed, sort_home_games_team))
	ha_per_game = [round(x, 2) for x in ha_per_game]

	ag_per_game = list(map(operator.truediv,
		sort_teams_ag_scored, sort_away_games_team))
	ag_per_game = [round(x, 2) for x in ag_per_game]

	aa_per_game = list(map(operator.truediv,
		sort_teams_ag_allowed, sort_away_games_team))
	aa_per_game = [round(x, 2) for x in aa_per_game]

		
	# Subtract goals allowed from goals scored to get goal diff
	home_goal_diff = list(map(operator.sub,
		hg_per_game, ha_per_game))
	
	away_goal_diff = list(map(operator.sub,
		ag_per_game, aa_per_game))

	# Plot home & away goal diff
	goal_diff = pygal.Bar(x_label_rotation=40)
	goal_diff.title = league_name + ' Teams Average Goal Difference Home and Away'
	goal_diff.x_labels = sort_teams
	goal_diff.add('Home GD', home_goal_diff)
	goal_diff.add('Away GD', away_goal_diff)
	goal_diff.render_in_browser()
	
	# Subtract away goal diff from home goal diff
	total_goal_diff = list(map(operator.sub,
		home_goal_diff, away_goal_diff))
	
	# Plot home & away goal diff
	tot_goal_diff = pygal.Bar(x_label_rotation=40)
	tot_goal_diff.title = league_name + ' Teams Average Difference in Home and Away GD'
	tot_goal_diff.x_labels = sort_teams
	tot_goal_diff.add('Home - Away GD',
		total_goal_diff)
	tot_goal_diff.render_in_browser()

	assert len(sort_teams) == len(sort_home_games_team)

