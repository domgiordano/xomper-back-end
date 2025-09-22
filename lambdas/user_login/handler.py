import asyncio
import json
import traceback
from lambdas.common.utility_helpers import build_successful_handler_response, build_error_handler_response, is_called_from_api, validate_dict
from lambdas.common.errors import UserDataError
from lambdas.common.constants import LOGGER
from user_data import login_user

log = LOGGER.get_logger(__file__)

HANDLER = 'user/login'

REQUIRED_FIELDS = ['userId', 'leagueId', 'password']

def handler(event, context):
    try:

        is_api = is_called_from_api(event)

        path = event.get("path").lower()
        headers = event.get("headers", {})
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
            return build_successful_handler_response(headers, response, is_api)

    except Exception as err:
        message = err.args[0]
        function = f'handler.{__name__}'
        if len(err.args) > 1:
            function = err.args[1]
        log.error(traceback.print_exc())
        error = UserDataError(message, HANDLER, function) if 'Invalid User Input' not in message else UserDataError(message, HANDLER, function, 400)
        return build_error_handler_response(headers, str(error))
