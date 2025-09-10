
from lambdas.common.constants import LOGGER, PLAYER_DATA_TABLE_NAME

from lambdas.common.sleeper_helper import fetch_nfl_players
from lambdas.common.dynamo_helpers import get_item_by_key

log = LOGGER.get_logger(__file__)

async def get_player_data(player_id: str):
    try:
        response = get_item_by_key(PLAYER_DATA_TABLE_NAME, "player_id",player_id)
        return response
    except Exception as err:
        log.error(f"Get Player Data: {err}")
        raise Exception(f"Get Player Data: {err}")