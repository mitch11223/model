from nba_api.stats.endpoints import playergamelog
import pandas as pd
import time


# Player IDs for the specific players
player_info = {
    'Aaron Gordon': {'id': '203932', 'team': 'DEN', 'position': 'PF'},
    'Alperen Sengun': {'id': '1630578', 'team': 'HOU', 'position': 'C'},
    'Anfernee Simons': {'id': '1629014', 'team': 'POR', 'position': 'PG'},
    'Anthony Davis': {'id': '203076', 'team': 'LAL', 'position': 'C'},
    'Anthony Edwards': {'id': '1630162', 'team': 'MIN', 'position': 'SG'},
    'Austin Reaves': {'id': '1630559', 'team': 'LAL', 'position': 'PG'},
    'Brandon Ingram': {'id': '1627742', 'team': 'NOP', 'position': 'SF'},
    'CJ McCollum': {'id': '203468', 'team': 'NOP', 'position': 'PG'},
    'Cade Cunningham': {'id': '1630595', 'team': 'DET', 'position': 'PG'},
    'Damian Lillard': {'id': '203081', 'team': 'MIL', 'position': 'PG'},
    'Darius Garland': {'id': '1629636', 'team': 'CLE', 'position': 'PG'},
    "De'Aaron Fox": {'id': '1628368', 'team': 'SAC', 'position': 'PG'},
    'Deandre Ayton': {'id': '1629028', 'team': 'POR', 'position': 'C'},
    'Desmond Bane': {'id': '1630217', 'team': 'MEM', 'position': 'SG'},
    'Devin Booker': {'id': '1626164', 'team': 'PHX', 'position': 'PG'},
    'Devin Vassell': {'id': '1630170', 'team': 'SAS', 'position': 'SG'},
    'Domantas Sabonis': {'id': '1627734', 'team': 'SAC', 'position': 'C'},
    'Donovan Mitchell': {'id': '1628378', 'team': 'CLE', 'position': 'SG'},
    'Immanuel Quickley': {'id': '1630193', 'team': 'TOR', 'position': 'SG'},
    'Ja Morant': {'id': '1629630', 'team': 'MEM', 'position': 'PG'},
    'Jabari Smith Jr': {'id': '1631095', 'team': 'HOU', 'position': 'PF'},
    'Jalen Brunson': {'id': '1628973', 'team': 'NYK', 'position': 'PG'},
    'Jalen Duren': {'id': '1631105', 'team': 'DET', 'position': 'C'},
    'Jalen Green': {'id': '1630224', 'team': 'HOU', 'position': 'SG'},
    'Jalen Williams': {'id': '1630583', 'team': 'OKC', 'position': 'SF'},
    'Jamal Murray': {'id': '1627750', 'team': 'DEN', 'position': 'PG'},
    'Jaren Jackson Jr': {'id': '1628991', 'team': 'MEM', 'position': 'PF'},
    'Jarrett Allen': {'id': '1628386', 'team': 'CLE', 'position': 'C'},
    'Jerami Grant': {'id': '203924', 'team': 'POR', 'position': 'PF'},
    'Joel Embiid': {'id': '203954', 'team': 'PHI', 'position': 'C'},
    'Jonas Valanciunas': {'id': '202685', 'team': 'NOP', 'position': 'C'},
    'Julius Randle': {'id': '203944', 'team': 'NYK', 'position': 'PF'},
    'Karl Anthony-Towns': {'id': '1626157', 'team': 'MIN', 'position': 'PF'},
    'Kawhi Leonard': {'id': '202695', 'team': 'LAC', 'position': 'SF'},
    'Keldon Johnson': {'id': '1629640', 'team': 'SAS', 'position': 'SF'},
    'Kentavious Caldwell-Pope': {'id': '203484', 'team': 'DEN', 'position': 'SG'},
    'Kevin Durant': {'id': '201142', 'team': 'PHX', 'position': 'PF'},
    'Kevon Looney': {'id': '1626172', 'team': 'GSW', 'position': 'C'},
    'Klay Thompson': {'id': '202691', 'team': 'GSW', 'position': 'SG'},
    'Kyrie Irving': {'id': '202681', 'team': 'DAL', 'position': 'SG'},
    'Lauri Markkanen': {'id': '1628374', 'team': 'UTA', 'position': 'PF'},
    'LeBron James': {'id': '2544', 'team': 'LAL', 'position':'PF'},
    'Luka Doncic': {'id': '1629029', 'team': 'DAL', 'position': 'PG'},
    'Marcus Smart': {'id': '203935', 'team': 'MEM', 'position': 'SG'},
    'Michael Porter Jr': {'id': '1629008', 'team': 'DEN', 'position': 'SF'},
    'Miles Bridges': {'id': '1628970', 'team': 'CHO', 'position': 'PF'},
    'OG Anunoby': {'id': '1628384', 'team': 'NYK', 'position': 'SF'},
    'Pascal Siakam': {'id': '1627783', 'team': 'TOR', 'position': 'PF'},
    'Scottie Barnes': {'id': '1630567', 'team': 'TOR', 'position': 'PG'},
    'Shaedon Sharpe': {'id': '1631101', 'team': 'POR', 'position': 'SG'},
    'Stephen Curry': {'id': '201939', 'team': 'GSW', 'position': 'PG'},
    'Tobias Harris': {'id': '202699', 'team': 'PHI', 'position': 'PF'},
    'Tyrese Maxey': {'id': '1630183', 'team': 'PHI', 'position': 'PG'},
    'Victor Wembanyama': {'id': '1641705', 'team': 'SAS', 'position': 'PF'},
    'Zion Williamson': {'id': '1629627', 'team': 'NOP', 'position': 'PF'}
}

def fetch_player_game_logs(player_id, season):
    try:
        game_logs = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        logs_df = game_logs.get_data_frames()[0]
        return logs_df
    except Exception as e:
        return f"Error: {e}"

def execute():
    for player, info in player_info.items():
        player_id = info['id']
        # Optionally use team and position info as needed
        # team = info['team']
        # position = info['position']

        time.sleep(1)
        result = fetch_player_game_logs(player_id, '2023-24')

        if isinstance(result, pd.DataFrame):
            result.to_csv(f"2023-24/gamelogs/{player}_log.txt", sep='\t', index=False)
            #print(f"{player} game log saved")
        else:
            print(f"Error fetching data for {player}: {result}")

