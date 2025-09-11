import asyncio
import traceback
from lambdas.common.utility_helpers import build_successful_handler_response, build_error_handler_response, is_called_from_api, validate_input
from lambdas.common.errors import PlayerDataError
from lambdas.common.constants import LOGGER
from player_data import get_player_data

log = LOGGER.get_logger(__file__)

HANDLER = 'player/data'


def handler(event, context):
    try:

        is_api = is_called_from_api(event)

        path = event.get("path").lower()
        body = event.get("body")
        http_method = event.get("httpMethod", "POST")
        response = None
        event_auth = event['headers']['Authorization']

        if path:
            log.info(f'Path called: {path} \nWith method: {http_method}')

            # Get Existing Player Data
            if (path == f"/{HANDLER}") and (http_method == 'GET'):

                query_string_parameters = event.get("queryStringParameters")

                if not validate_input(query_string_parameters, {'playerId'}):
                    raise Exception("Invalid User Input - missing required field or contains extra field.")

                response = asyncio.run(get_player_data(query_string_parameters['playerId']))

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
        error = PlayerDataError(message, HANDLER, function) if 'Invalid User Input' not in message else PlayerDataError(message, HANDLER, function, 400)
        return build_error_handler_response(str(error))
