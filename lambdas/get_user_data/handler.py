import asyncio
import traceback
from lambdas.common.utility_helpers import send_proxy_response, is_called_from_api, validate_dict
from lambdas.common.errors import UserDataError
from lambdas.common.constants import LOGGER
from user_data import get_user_data

log = LOGGER.get_logger(__file__)

HANDLER = 'user/data'
BASE_MSG = "Get User Data"

def handler(event, context):
    try:

        path = event.get("path").lower()
        http_method = event.get("httpMethod", "POST")
        response = None

        log.info(f'Path called: {path} \nWith method: {http_method}')
            
        query_string_parameters = event.get("queryStringParameters")

        validate_dict(query_string_parameters, {'userId'})
        
        response = asyncio.run(get_user_data(query_string_parameters['userId']))
        log.info("Sleeper user found and loaded.")
                

        if response is None:
            raise Exception(f"{BASE_MSG} Unexepected Error.")
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
