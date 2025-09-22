
import datetime
import decimal
import json
import logging
from urllib3.connection import HTTPConnection
import base64

# Used to ensure we dump our JSON out with a decimal decoder, so that it gets logged okay if a decimal.
from lambdas.common.constants import LOGGER, RESPONSE_HEADERS

log = LOGGER.get_logger(__file__)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)


def is_called_from_api(event):
    # If body is not a dict, we'll assume it's a string from API Gateway
    return type(event['body']) != dict


def extract_body_from_event(event, is_api):
    if is_api:
        return json.loads(event.get('body'))
    else:
        return event.get('body')

def build_successful_handler_response(body_object: dict, is_api):
    return {
        'statusCode': 200,
        'headers': RESPONSE_HEADERS,
        'body': json.dumps(body_object, cls=DecimalEncoder) if is_api else body_object,
        "isBase64Encoded": False
    }


def build_error_handler_response(error, is_api: bool = True):
    error_dict = json.loads(error)
    status = error_dict['status']
    del error_dict['status']
    body_object = {"error": error_dict}
    return {
        'statusCode': status,
        'headers': RESPONSE_HEADERS,
        'body': json.dumps(body_object, cls=DecimalEncoder) if is_api else body_object,
        "isBase64Encoded": False
    }


def set_response(statusCode, body):
    return {
        "statusCode": statusCode or 500,
        "headers": {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"},
        "body": body or {"error": {"message": "Something went wrong..."}},
        "isBase64Encoded": False
    }


def log_handler_error(friendly_error_msg, err_args_text, calling_module):
    # logging configuration:
    friendly_error_msg = "log_error called from {0}! FRIENDLY MESSAGE: {1}".format(
        calling_module, friendly_error_msg)
    err_args_text = "log_error called from {0}! ERR ARGS: {1}".format(
        calling_module, err_args_text)

    logger = logging.getLogger()
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - line #: %(lineno)d - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    HTTPConnection.debuglevel = 1

    # Actually perform the logging...
    logger.error(friendly_error_msg)
    logger.error(err_args_text)

def request_on_long():
    """Format = YYYY-MM-DD - Example: 2022-03-02"""

    time_now = datetime.datetime.utcnow()
    date_now = time_now.strftime('%Y-%m-%d')
    return date_now


def request_time():
    """Format = PTAHBMCS where A, B, and C are hours, mins, seconds - Example: PT16H19M10S"""

    time_now = datetime.datetime.utcnow()
    requested_time_template = "PT{}H{}M{}S"
    return requested_time_template.format(time_now.strftime('%H'), time_now.strftime('%M'), time_now.strftime('%S'))


def encoded_key(consumer_key, consumer_secret):
    """Rest authentication for Basic Auth Encoding."""
    data = "%s:%s" % (consumer_key, consumer_secret)
    encoded_bytes = base64.b64encode(data.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    return encoded_str

def format_date(raw_date):
    date_mdy = raw_date.split('/')
    date = datetime.datetime(int(date_mdy[2]), int(date_mdy[0]), int(date_mdy[1]))
    return date

def validate_dict(data: dict, required_fields: dict = {}, optional_fields: dict = {}):
    try:
        data_keys = data.keys()
        all_fields = set(required_fields) | set(optional_fields)

        # Missing Req Fields
        if required_fields - data_keys:
            log.error("Invalid API Call - Missing Required Fields")
            raise Exception("Invalid Call: Missing Required Fields.")
        
        # Check for blank values
        for field in required_fields:
            if not data[field]:
                log.error(f"Invalid API Call - Required field {field} has a blank value")
                raise Exception(f"Invalid Call: Required field {field} cannot be empty.")
            
        # Additional Fields
        if data_keys - all_fields:
            log.error(f"Invalid API Call - Extra Fields")
            raise Exception(f"Invalid Call: Extra Fields")
        
        log.info("Valid API fields.")
    except Exception as err:
        log.error(f"Validate Dict: {err}")
        raise Exception(f"Validate Dict: {err}") from err