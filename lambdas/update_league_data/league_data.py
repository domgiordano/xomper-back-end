from decimal import Decimal
import json
from lambdas.common.constants import LOGGER, LEAGUE_DATA_TABLE_NAME

from lambdas.common.sleeper_helper import get_sleeper_league
from lambdas.common.dynamo_helpers import update_table_item

log = LOGGER.get_logger(__file__)

async def update_league_data(league_id: str) -> dict:
    try:
        sleeper_league = await get_sleeper_league(league_id)
        league = json.loads(json.dumps(sleeper_league), parse_float=Decimal)
        update_table_item(LEAGUE_DATA_TABLE_NAME, league)
        return f"League {league_id} updated in table."
        
    except Exception as err:
        log.error(f"Update Sleeper League: {err}")
        raise Exception(f"Update Sleeper League: {err}")