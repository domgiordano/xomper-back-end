
from lambdas.common.constants import LOGGER, USER_DATA_TABLE_NAME

from lambdas.common.sleeper_helper import get_sleeper_user
from lambdas.common.dynamo_helpers import update_table_item

log = LOGGER.get_logger(__file__)

def update_user_data(user_id: str) -> dict:
    try:
        sleeper_user = get_sleeper_user(user_id)
        update_table_item(USER_DATA_TABLE_NAME, sleeper_user)
        return f"User {user_id} updated in table."
        
    except Exception as err:
        log.error(f"Update Sleeper User: {err}")
        raise Exception(f"Update Sleeper User: {err}")