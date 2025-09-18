import json
from decimal import Decimal
from lambdas.common.constants import LOGGER, USER_DATA_TABLE_NAME

from lambdas.common.sleeper_helper import get_sleeper_user
from lambdas.common.dynamo_helpers import update_table_item

log = LOGGER.get_logger(__file__)

async def update_user_data(user_id: str) -> dict:
    try:
        sleeper_user = await get_sleeper_user(user_id)
        user = json.loads(json.dumps(sleeper_user), parse_float=Decimal)
        update_table_item(USER_DATA_TABLE_NAME, user)
        return f"User {user_id} updated in table."
        
    except Exception as err:
        log.error(f"Update Sleeper User: {err}")
        raise Exception(f"Update Sleeper User: {err}")