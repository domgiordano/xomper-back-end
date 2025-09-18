
from lambdas.common.constants import LOGGER

from lambdas.common.sleeper_helper import get_sleeper_user

log = LOGGER.get_logger(__file__)

async def get_user_data(user_id: str) -> dict:
    try:
        sleeper_user = get_sleeper_user(user_id)
        return sleeper_user
        
    except Exception as err:
        log.error(f"Get Sleeper User: {err}")
        raise Exception(f"Get Sleeper User: {err}")