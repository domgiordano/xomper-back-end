
from lambdas.common.constants import LOGGER, PLAYER_DATA_TABLE_NAME

from lambdas.common.sleeper_helper import fetch_nfl_players
from lambdas.common.dynamo_helpers import batch_write_table_items

log = LOGGER.get_logger(__file__)

async def player_data_chron_job():
    try:
        players = fetch_nfl_players()
        response = batch_write_table_items(PLAYER_DATA_TABLE_NAME, players)
        return response
    except Exception as err:
        log.error(f"Player Data Chron Job: {err}")
        raise Exception(f"Player Data Chron Job: {err}")