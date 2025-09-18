
from lambdas.common.constants import LOGGER, LEAGUE_DATA_TABLE_NAME

from lambdas.common.sleeper_helper import get_sleeper_league
from lambdas.common.dynamo_helpers import update_table_item

log = LOGGER.get_logger(__file__)

def update_league_data(league_id: str) -> dict:
    try:
        sleeper_league = get_sleeper_league(league_id)
        update_table_item(LEAGUE_DATA_TABLE_NAME, sleeper_league)
        return f"League {league_id} updated in table."
        
    except Exception as err:
        log.error(f"Update Sleeper League: {err}")
        raise Exception(f"Update Sleeper League: {err}")