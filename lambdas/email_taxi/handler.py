"""
POST /email/rule-proposal - Send Taxi Squad Email
"""
import asyncio
from lambdas.common.logger import get_logger
from lambdas.common.errors import handle_errors
from lambdas.common.utility_helpers import success_response, parse_body, require_fields

log = get_logger(__file__)

HANDLER = 'email_taxi'

@handle_errors(HANDLER)
def handler(event, context):
    log.info("📧 Starting Send Taxi Squad Email...")
    body = parse_body(event)
    require_fields(body, 'user', 'targetUser', 'player', 'emails')

    user = body.get('user')
    target_user = body.get('targetUser')
    player = body.get('player')
    emails = body.get('emails')

    log.info(f"User {user} is stealing a player from {target_user}'s taxi squad. \n Sending emails to league members: {emails}")

    successes, failures = 0,0 # Return successful and failure emails

    return success_response({
        "successfulEmails": successes,
        "failedEmails": failures
    }, is_api=False)