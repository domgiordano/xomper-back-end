"""
POST /email/rule-deny - Send Rule Deny Email
"""

from lambdas.common.logger import get_logger
from lambdas.common.errors import handle_errors
from lambdas.common.utility_helpers import success_response, parse_body, require_fields

log = get_logger(__file__)

HANDLER = 'email_rule_deny'


@handle_errors(HANDLER)
def handler(event, context):
    log.info("📧 Starting Send Rule Denial Email...")
    body = parse_body(event)
    require_fields(body, 'user', 'rule', 'approved', 'rejected', 'emails')

    user = body.get('user')
    rule = body.get('rule')
    approved = body.get('approved')
    rejected = body.get('rejected')
    emails = body.get('emails')

    log.info(f"User {user} proposed rule {rule} DENIED. \n Approved: {len(approved)}, Rejected: {len(rejected)} \n Sending emails to league members: {emails}")

    successes, failures = 0,0 # Return successful and failure emails

    return success_response({
        "successfulEmails": successes,
        "failedEmails": failures
    }, is_api=False)