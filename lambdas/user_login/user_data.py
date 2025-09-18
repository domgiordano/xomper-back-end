
from lambdas.common.constants import LOGGER, USER_DATA_TABLE_NAME, LEAGUE_DATA_TABLE_NAME

from lambdas.common.dynamo_helpers import get_item_by_key
from lambdas.common.sleeper_helper import get_sleeper_user

log = LOGGER.get_logger(__file__)

async def login_user(data: dict) -> dict:
    try:
        # Get Vals
        user_id = data['userId']
        league_id = data['leagueId']
        password = data['password']
        user = get_item_by_key(USER_DATA_TABLE_NAME, 'user_id', user_id)
        if not user:
            log.warning("User not found for username and league. Block Login.")
            return {}
        elif user['password'] == password:
            log.info("User password matches. Validating user in Sleeper League.")
            sleeper_user = get_sleeper_user(user_id)
            league = get_item_by_key(LEAGUE_DATA_TABLE_NAME, 'league_id', league_id)
            if sleeper_user['id'] in league['user_ids']:
                log.info("User is in league. Login Successful.")
                return sleeper_user
            else:
                log.warning("User is not in league. Login Blocked.")
                return {}
        else:
            log.warning("User exists but password does not match. Block login.")
            return {}
        
    except Exception as err:
        log.error(f"Login User: {err}")
        raise Exception(f"Login User: {err}")