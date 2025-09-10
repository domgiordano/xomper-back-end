import requests

import json
import sqlite3  # Example database, can be replaced with PostgreSQL/MySQL
from lambdas.common.constants import LOGGER

log = LOGGER.get_logger(__file__)

def fetch_nfl_players():
    try:
        url = "https://api.sleeper.app/v1/players/nfl"
        response = requests.get(url)

        if response.status_code == 200:
            players = response.json()  # JSON is a dict with player IDs as keys
            return players
        else:
            raise Exception(response.status_code)
    except Exception as err:
        log.error(f"Error Fetching NFL Players:  {err}")
        raise Exception(f"Error Fetching NFL Players:  {err}")
    
def __format_players(players: dict):
    return [data for player_id, data in players.items()]

