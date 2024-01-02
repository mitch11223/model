import requests
from bs4 import BeautifulSoup
import player_averagesanddvpos_condenser as cond
import time

playing_today = cond.playing_today
date = time.strftime("%d-%m-%Y")
filename = f"2023-24/projections/{date}.txt"


def calculate_projection(player_data, stat):
    # Calculate the 'minutes_weighting' factor
    minutes_weighting = float(player_data['averages']['MIN']) / 48

    # Initialize total projection
    total_projection = 0

    # Calculate partial projections from last 7, 15, and 30 day stats
    for timeframe in ['7_days', '15_days', '30_days']:
        if timeframe == '7_days':
            weight = 0.175
        elif timeframe == '15_days':
            weight = 0.075
        elif timeframe == '30_days':
            weight = 0.05
        if stat == 'PTS':
            conv_stat = 'points'
        elif stat == 'AST':
            conv_stat = 'assists'
        elif stat == 'REB':
            conv_stat = 'rebounds'

        timeframe_stat = player_data['defense_stats'].get(timeframe, {}).get(conv_stat, 0)
        #total_projection += ((timeframe_stat * minutes_weighting) * weight)
        total_projection += ((timeframe_stat) * weight)
        

    # Calculate and add the projection from average stats
    average_stat = float(player_data['averages'].get(stat, 0))
    total_projection += (average_stat * 0.7)

    return round(total_projection,2)

def execute():
    with open(filename,"w+") as file:
        file.write('player,points,rebounds,assists,prop_points,prop_rebounds,prop_assists,points_diff,rebounds_diff,assists_diff' + '\n')
        # Iterating through all players in 'playing_today'
        for player_data in playing_today:
            player = player_data['player']
            points_projection = calculate_projection(player_data, 'PTS')
            rebounds_projection = calculate_projection(player_data, 'REB')
            assists_projection = calculate_projection(player_data, 'AST')
            file.write(f"{player},{points_projection},{rebounds_projection},{assists_projection}, , , , , , " + '\n')
            
            print(f"Projections for {player_data['player']}: Points: {points_projection}, Rebounds: {rebounds_projection}, Assists: {assists_projection}")
