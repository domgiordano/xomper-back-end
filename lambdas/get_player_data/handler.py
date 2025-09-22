import asyncio
import traceback
from lambdas.common.utility_helpers import send_proxy_response, validate_dict
from lambdas.common.errors import PlayerDataError
from lambdas.common.constants import LOGGER
from player_data import get_player_data

log = LOGGER.get_logger(__file__)

HANDLER = 'player/data'
BASE_MSG = "Get Player Data"


def handler(event, context):
    try:

        path = event.get("path").lower()
        http_method = event.get("httpMethod", "POST")
        response = None

        log.info(f'Path called: {path} \nWith method: {http_method}')


        query_string_parameters = event.get("queryStringParameters")

        validate_dict(query_string_parameters, {'playerId'})
            
        response = asyncio.run(get_player_data(query_string_parameters['playerId']))

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
        error = PlayerDataError(message, HANDLER, function) if 'Invalid User Input' not in message else PlayerDataError(message, HANDLER, function, 400)
        return send_proxy_response(False, error.status, f"{BASE_MSG} Failure.", error.message)
