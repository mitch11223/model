from nba_api.live.nba.endpoints import scoreboard
import player_gamelog_getter as pgg
import pandas as pd
import json
import csv

# Use NBA API to find games
todays_games = scoreboard.ScoreBoard().games.get_dict()

# List of JSON files with defense stats
defense_vpos_filenames = ['2023-24/defense_vpos/team_defense_vpos_7.json', 
                          '2023-24/defense_vpos/team_defense_vpos_15.json', 
                          '2023-24/defense_vpos/team_defense_vpos_30.json']

def load_defense_stats(defense_filenames):
    defense_stats = {}
    for filename in defense_filenames:
        timeframe = filename.split('_')[-1].split('.')[0]  # Extracts '7', '15', or '30' from filename
        with open(filename, 'r') as file:
            data = json.load(file)
            for team_code, position_stats in data['teams'].items():
                if team_code not in defense_stats:
                    defense_stats[team_code] = {}
                if timeframe not in defense_stats[team_code]:
                    defense_stats[team_code][timeframe] = {}
                defense_stats[team_code][timeframe].update(position_stats)
    return defense_stats

# Load defense stats
defense_stats = load_defense_stats(defense_vpos_filenames)

def get_players_playing_today(player_info, todays_games, defense_stats):
    playing_today = []
    base_path = '2023-24/averages/'
    for player, details in player_info.items():
        player_team = details['team']
        for game in todays_games:
            if player_team in [game['homeTeam']['teamTricode'], game['awayTeam']['teamTricode']]:
                opponent_team = game['awayTeam']['teamTricode'] if player_team == game['homeTeam']['teamTricode'] else game['homeTeam']['teamTricode']
                if opponent_team == 'NOP':  # Handle specific team code case
                    opponent_team = 'NOR'
                if opponent_team == 'PHX':
                    opponent_team = 'PHO'
               
                home_away = 'home' if player_team == game['homeTeam']['teamTricode'] else 'away'
                defense_stats_aggregated = {'7_days': {}, '15_days': {}, '30_days': {}}
                if opponent_team in defense_stats:
                    for timeframe in ['7', '15', '30']:
                        if details['position'] in defense_stats[opponent_team].get(timeframe, {}):
                            defense_stats_aggregated[f'{timeframe}_days'] = defense_stats[opponent_team][timeframe][details['position']]

                # Read player's average stats
                player_avg_file = f'{base_path}{player}_log.txt'
                try:
                    with open(player_avg_file, 'r') as file:
                        csv_reader = csv.DictReader(file)
                        player_averages = next(csv_reader)  # Assuming the first row contains the required averages
                except FileNotFoundError:
                    print(f"Average stats file for {player} not found.")
                    player_averages = {}

                player_entry = {
                    'player': player,
                    'opponent': opponent_team,
                    'home_away': home_away,
                    'defense_stats': defense_stats_aggregated,
                    'averages': player_averages
                }
                playing_today.append(player_entry)
    return playing_today



# Call the function with the loaded data
playing_today = get_players_playing_today(pgg.player_info, todays_games, defense_stats)


