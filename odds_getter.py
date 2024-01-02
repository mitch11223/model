import requests
from bs4 import BeautifulSoup
import player_averagesanddvpos_condenser as cond

playing_today = cond.playing_today

print(playing_today[0])

def get_player_stat_url(player_name, stat):
    """Format the URL for the player's stat."""
    base_url = "https://www.bettingpros.com/nba/props/"
    formatted_name = player_name.lower().replace(" ", "-")
    return f"{base_url}{formatted_name}/{stat}/"

def fetch_odds(url):
    """Fetch the odds for a given player and stat."""
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML and extract the betting odds here...
        # This will depend on the HTML structure of the page.
        soup = BeautifulSoup(response.text, 'html.parser')
        # Example: Find a specific element containing the odds
        odds_element = soup.find('div', class_='odds-class') 
        return odds_element.text if odds_element else "Odds not found"
    
    else:
        return "Failed to fetch data"

def main():
    for player in playing_today:
        url = get_player_stat_url(player['player'], player['stat'])
        odds = fetch_odds(url)
        print(f"Odds for {player['name']} ({player['stat']}): {odds}")


main()
