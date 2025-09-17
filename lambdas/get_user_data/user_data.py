
from lambdas.common.constants import LOGGER, USER_DATA_TABLE_NAME

from lambdas.common.dynamo_helpers import get_item_by_multiple_keys
from lambdas.common.sleeper_helper import get_sleeper_user

log = LOGGER.get_logger(__file__)

async def get_user_data(data: dict) -> dict:
    try:
        # Get Vals
        user_id = data['userId']
        league_id = data['league_id']
        password = data['password']
        user = get_item_by_multiple_keys(USER_DATA_TABLE_NAME, 'user_id', user_id, 'league_id', league_id)
        if not user:
            log.warning("User not found for username and league. Block Login.")
            return {}
        elif user['password'] == password:
            log.info("User exists and password matches. Fetching Sleeper data.")
            return get_sleeper_user(user_id)
        else:
            log.warning("User exists but password does not match. Block login.")
            return {}
        
        
        return user
    except Exception as err:
        log.error(f"Get Player Data: {err}")
        raise Exception(f"Get Player Data: {err}")