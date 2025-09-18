import json
import traceback
from lambdas.common.utility_helpers import build_successful_handler_response, build_error_handler_response, is_called_from_api, validate_dict
from lambdas.common.errors import UserDataError
from lambdas.common.constants import LOGGER
from user_data import update_user_data

log = LOGGER.get_logger(__file__)

HANDLER = 'user/data'

def handler(event, context):
    try:

        is_api = is_called_from_api(event)

        path = event.get("path").lower()
        body = json.loads(event.get("body"))
        http_method = event.get("httpMethod", "POST")
        response = None
        event_auth = event['headers']['Authorization']

        if path:
            log.info(f'Path called: {path} \nWith method: {http_method}')

            # Get Existing Player Data
            if (path == f"/{HANDLER}") and (http_method == 'POST'):

                if not validate_dict(body, {'userId'}):
                    raise Exception("Invalid User Input - missing required field or contains extra field.")
                
                response = update_user_data(body['userId'])
                
        if response is None:
            raise Exception("Invalid Call.", 400)
        else:
            return build_successful_handler_response(response, is_api)

    except Exception as err:
        message = err.args[0]
        function = f'handler.{__name__}'
        if len(err.args) > 1:
            function = err.args[1]
        log.error(traceback.print_exc())
        error = UserDataError(message, HANDLER, function) if 'Invalid User Input' not in message else UserDataError(message, HANDLER, function, 400)
        return build_error_handler_response(str(error))
