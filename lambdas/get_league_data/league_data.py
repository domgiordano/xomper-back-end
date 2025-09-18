import asyncio
from lambdas.common.constants import LOGGER

from lambdas.common.sleeper_helper import get_sleeper_league, get_sleeper_league_rosters, get_sleeper_league_users

log = LOGGER.get_logger(__file__)

async def get_league_data(league_id: str) -> dict:
    try:
        tasks = [
            get_sleeper_league(league_id),
            get_sleeper_league_users(league_id),
            get_sleeper_league_rosters(league_id)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                raise Exception(result)
        # Returns League, Users, Rosters
        return results[0], results[1], results[2]
        
    except Exception as err:
        log.error(f"Get Sleeper League: {err}")
        raise Exception(f"Get Sleeper League: {err}")