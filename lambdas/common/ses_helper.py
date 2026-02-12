import asyncio
import boto3
from botocore.exceptions import ClientError
from lambdas.common.constants import FROM_EMAIL, AWS_DEFAULT_REGION
from lambdas.common.logger import get_logger

log = get_logger(__file__)

ses_client = boto3.client('ses', region_name=AWS_DEFAULT_REGION)


def send_email(to_email: str, subject: str, html_body: str, text_body: str, tags: list = None) -> bool:
    """Send an email via AWS SES. Returns True on success, False on failure."""
    try:
        response = ses_client.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Text': {'Data': text_body, 'Charset': 'UTF-8'},
                    'Html': {'Data': html_body, 'Charset': 'UTF-8'},
                },
            },
            Tags=tags or [],
        )
        log.info(f"Email sent to {to_email}, MessageId: {response.get('MessageId')}")
        return True
    except ClientError as err:
        error = err.response['Error']
        log.error(f"SES error sending to {to_email}: {error['Code']} - {error['Message']}")
        return False
    except Exception as err:
        log.error(f"Error sending email to {to_email}: {err}")
        return False


def send_emails_concurrently(email_tasks: list) -> tuple:
    """
    Send multiple emails concurrently using asyncio.

    Args:
        email_tasks: List of (to_email, subject, html_body, text_body) tuples

    Returns:
        Tuple of (successes, failures)
    """
    async def _send(to_email, subject, html_body, text_body):
        return await asyncio.to_thread(send_email, to_email, subject, html_body, text_body)

    async def _run():
        return await asyncio.gather(*[_send(*task) for task in email_tasks])

    results = asyncio.run(_run())
    successes = sum(1 for r in results if r)
    return successes, len(results) - successes
