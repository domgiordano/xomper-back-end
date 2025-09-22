import asyncio
import traceback
from lambdas.common.utility_helpers import send_proxy_response, validate_dict
from lambdas.common.errors import LeagueDataError
from lambdas.common.constants import LOGGER
from lambdas.get_league_data.league_data import get_league_data

log = LOGGER.get_logger(__file__)

HANDLER = 'league/data'
BASE_MSG = "Get League Data"

def handler(event, context):
    try:

        path = event.get("path").lower()
        http_method = event.get("httpMethod", "POST")
        response = None

        if path:
            log.info(f'Path called: {path} \nWith method: {http_method}')

            # Get Existing League Data
            if (path == f"/{HANDLER}") and (http_method == 'GET'):
                
                query_string_parameters = event.get("queryStringParameters")

                validate_dict(query_string_parameters, {'leagueId'})
                
                league, league_users, league_rosters = asyncio.run(get_league_data(query_string_parameters['leagueId']))
                log.info("Sleeper league found and loaded.")
                response = {
                    "league": league,
                    "leagueUsers": league_users,
                    "leagueRosters": league_rosters
                }
                

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
        error = LeagueDataError(message, HANDLER, function) if 'Invalid User Input' not in message else LeagueDataError(message, HANDLER, function, 400)
        return send_proxy_response(False, error.status, f"{BASE_MSG} Failure.", error.message)
