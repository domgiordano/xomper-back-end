from decimal import Decimal
import asyncio
import json
from lambdas.common.constants import LOGGER, LEAGUE_DATA_TABLE_NAME

from lambdas.common.sleeper_helper import get_sleeper_league, get_sleeper_league_users
from lambdas.common.dynamo_helpers import update_table_item

log = LOGGER.get_logger(__file__)

async def update_league_data(league_id: str) -> dict:
    try:
        tasks = [
            get_sleeper_league(league_id),
            get_sleeper_league_users(league_id)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                raise Exception(result)
            
        sleeper_league = results[0]
        sleeper_league_users = results[1]
        sleeper_league_users_ids = [user['user_id'] for user in sleeper_league_users]
        sleeper_league["user_ids"] = sleeper_league_users_ids
        league = json.loads(json.dumps(sleeper_league), parse_float=Decimal)
        update_table_item(LEAGUE_DATA_TABLE_NAME, league)
        return f"League {league_id} updated in table."
        
    except Exception as err:
        log.error(f"Update Sleeper League: {err}")
        raise Exception(f"Update Sleeper League: {err}")