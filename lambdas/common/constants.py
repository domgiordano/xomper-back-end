import os
from lambdas.common.logger import Logger

# General
AWS_DEFAULT_REGION ='us-east-1'
AWS_ACCOUNT_ID = os.environ['AWS_ACCOUNT_ID']
PRODUCT = 'xomper'

# Headers
RESPONSE_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    "Content-Type": "application/json"
}

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOGGER = Logger(LOG_LEVEL)

# Dynamodb
DYNAMODB_KMS_ALIAS = os.environ['DYNAMODB_KMS_ALIAS']
PLAYER_DATA_TABLE_NAME = os.environ['PLAYER_DATA_TABLE_NAME']
