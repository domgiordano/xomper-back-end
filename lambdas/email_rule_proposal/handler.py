"""
POST /email/taxi - Send Rule Proposal Email
"""

from lambdas.common.logger import get_logger
from lambdas.common.errors import handle_errors
from lambdas.common.utility_helpers import success_response, parse_body, require_fields

log = get_logger(__file__)

HANDLER = 'email_rule_proposal'

@handle_errors(HANDLER)
def handler(event, context):
    log.info("📧 Starting Send Rule Proposal Email...")
    body = parse_body(event)
    require_fields(body, 'user', 'rule', 'emails')

    user = body.get('user')
    rule = body.get('rule')
    emails = body.get('emails')

    log.info(f"User {user} is proposing rule {rule}. \n Sending emails to league members: {emails}")

    successes, failures = 0,0 # Return successful and failure emails

    return success_response({
        "successfulEmails": successes,
        "failedEmails": failures
    }, is_api=False)