import logging

import httpx

from socialapi.core.config import config
from socialapi.exceptions.exceptions import MailResponseException

logger = logging.getLogger(__name__)


async def send_email(to: str, subject: str, body: str, html: str = None):
    logger.info(f"Sending email to {to}")

    async with httpx.AsyncClient() as client:
        try:
            data = {
                "from": f"{config.APP_NAME} <postmaster@{config.MAILGUN_DOMAIN}>",
                "to": [to],
                "subject": subject,
                "text": body,
            }
            if html:
                data["html"] = html

            response = await client.post(
                f"{config.MAILGUN_URI}/{config.MAILGUN_DOMAIN}/messages",
                auth=(
                    "api",
                    config.MAILGUN_API_KEY,
                ),
                data=data,
            )
            response.raise_for_status()

            return response
        except httpx.HTTPStatusError as e:
            logger.error(f"Error sending email: {e}")
            raise MailResponseException("Error sending email") from e
