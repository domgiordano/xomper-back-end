"""
POST /email/rule-accept - Send Rule Accepted Email
Notifies all league members that a rule has been approved.

Expected body:
{
    "proposal": {
        "title": "Allow IR stashing",
        "description": "Players on IR can be stashed...",
        "proposed_by_username": "Dom"
    },
    "approved_by": ["Dom", "Steve", "Mike"],
    "rejected_by": ["Jake"],
    "recipients": ["email1@...", "email2@..."]
}
"""
from lambdas.common.logger import get_logger
from lambdas.common.errors import handle_errors
from lambdas.common.utility_helpers import success_response, parse_body, require_fields
from lambdas.common.ses_helper import send_emails_concurrently
from lambdas.common.constants import XOMPER_URL
from lambdas.common.email_templates import (
    generate_rule_accepted_email,
    generate_rule_accepted_email_plain_text,
)

log = get_logger(__file__)

HANDLER = 'email_rule_accept'


@handle_errors(HANDLER)
def handler(event, context):
    log.info("Starting Send Rule Accepted Email...")
    body = parse_body(event)
    require_fields(body, 'proposal', 'approved_by', 'rejected_by', 'recipients')

    proposal = body['proposal']
    approved_by = body['approved_by']
    rejected_by = body['rejected_by']
    recipients = body['recipients']

    proposer_name = proposal.get('proposed_by_username', 'A league member')
    rule_title = proposal.get('title', 'Untitled Rule')
    rule_description = proposal.get('description', '')

    log.info(f"Rule '{rule_title}' ACCEPTED. {len(approved_by)} yes, {len(rejected_by)} no. Notifying {len(recipients)} members.")

    subject = f"Rule APPROVED: {rule_title}"
    html_body = generate_rule_accepted_email(
        proposer_name=proposer_name,
        rule_title=rule_title,
        rule_description=rule_description,
        approved_voters=approved_by,
        rejected_voters=rejected_by,
        league_url=XOMPER_URL,
    )
    text_body = generate_rule_accepted_email_plain_text(
        proposer_name=proposer_name,
        rule_title=rule_title,
        rule_description=rule_description,
        approved_voters=approved_by,
        rejected_voters=rejected_by,
        league_url=XOMPER_URL,
    )

    tasks = [(email, subject, html_body, text_body) for email in recipients]
    successes, failures = send_emails_concurrently(tasks)
    log.info(f"Rule accepted emails complete: {successes} sent, {failures} failed")

    return success_response({
        "successfulEmails": successes,
        "failedEmails": failures
    }, is_api=False)
