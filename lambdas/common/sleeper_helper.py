import requests

from lambdas.common.constants import LOGGER

log = LOGGER.get_logger(__file__)
SLEEPER_URL_BASE = "https://api.sleeper.app/v1"

def fetch_nfl_players():
    try:
        url = f"{SLEEPER_URL_BASE}/players/nfl"
        response = requests.get(url)

        if response.status_code == 200:
            players = response.json()  # JSON is a dict with player IDs as keys
            return players
        else:
            raise Exception(response.status_code)
    except Exception as err:
        log.error(f"Error Fetching NFL Players:  {err}")
        raise Exception(f"Error Fetching NFL Players:  {err}")
    
def get_sleeper_user(user_id: str):
    try:
        url = f"{SLEEPER_URL_BASE}/user/{user_id}"
        response = requests.get(url)

        if response.status_code == 200:
            user = response.json()  # JSON is a dict with player IDs as keys
            return user
        else:
            raise Exception(response.status_code)
    except Exception as err:
        log.error(f"Error Getting Sleeper User:  {err}")
        raise Exception(f"Error Getting Sleeper User:  {err}")
    
async def get_sleeper_league(league_id: str):
    try:
        url = f"{SLEEPER_URL_BASE}/league/{league_id}"
        response = requests.get(url)

        if response.status_code == 200:
            league = response.json()  
            return league
        else:
            raise Exception(response.status_code)
    except Exception as err:
        log.error(f"Error Getting League:  {err}")
        raise Exception(f"Error Getting League:  {err}")
    
async def get_sleeper_league_rosters(league_id: str):
    try:
        url = f"{SLEEPER_URL_BASE}/league/{league_id}/rosters"
        response = requests.get(url)

        if response.status_code == 200:
            league = response.json()  
            return league
        else:
            raise Exception(response.status_code)
    except Exception as err:
        log.error(f"Error Getting League Rosters:  {err}")
        raise Exception(f"Error Getting League Rosters:  {err}")
    
async def get_sleeper_league_users(league_id: str):
    try:
        url = f"{SLEEPER_URL_BASE}/league/{league_id}/users"
        response = requests.get(url)

        if response.status_code == 200:
            league = response.json()  
            return league
        else:
            raise Exception(response.status_code)
    except Exception as err:
        log.error(f"Error Getting League Users:  {err}")
        raise Exception(f"Error Getting League Users:  {err}")
    
def __format_players(players: dict):
    return [data for player_id, data in players.items()]

