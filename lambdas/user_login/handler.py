import asyncio
import json
import traceback
from lambdas.common.utility_helpers import send_proxy_response, validate_dict
from lambdas.common.errors import UserDataError
from lambdas.common.constants import LOGGER
from user_data import login_user

log = LOGGER.get_logger(__file__)

HANDLER = 'user/login'
BASE_MSG = "User Login"

REQUIRED_FIELDS = ['userId', 'leagueId', 'password']

def handler(event, context):
    try:

        path = event.get("path").lower()
        body = json.loads(event.get("body")) if type(event.get("body")) == str else event.get("body")
        http_method = event.get("httpMethod", "POST")
        response = None

        if path:
            log.info(f'Path called: {path} \nWith method: {http_method}')

            # Get Existing Player Data
            if (path == f"/{HANDLER}") and (http_method == 'POST'):

                validate_dict(body, REQUIRED_FIELDS)

                response = asyncio.run(login_user(body))
                log.info("Sleeper user found and logged in.")
                

        if response is None:
            raise Exception("Invalid Call.", 400)
        else:
            return send_proxy_response(True, 200, f"{BASE_MSG} Success.", response)

    except Exception as err:
        message = err.args[0]
        function = f'handler.{__name__}'
        if len(err.args) > 1:
            function = err.args[1]
        log.error(traceback.print_exc())
        error = UserDataError(message, HANDLER, function) if 'Invalid User Input' not in message else UserDataError(message, HANDLER, function, 400)
        return send_proxy_response(False, error.status, f"{BASE_MSG} Failure.", error.message)
