import logging

from fastapi import BackgroundTasks

from socialapi.core.config import config
from socialapi.core.security import (
    create_confirmation_token,
    create_password_reset_token,
)
from socialapi.core.tasks import send_email
from socialapi.exceptions.exceptions import MailResponseException
from socialapi.models.user import User

logger = logging.getLogger(__name__)


async def create_confirmation_url(email: str):
    return f"{config.FRONT_URL}/confirm-email/{create_confirmation_token(email)}"


async def create_password_reset_url(email: str):
    return f"{config.FRONT_URL}/reset-password/{create_password_reset_token(email)}"


def send_confirmation_email(user: User, background_tasks: BackgroundTasks):
    background_tasks.add_task(_send_confirmation_email_task, user)


async def _send_confirmation_email_task(user: User):
    confirmation_url = await create_confirmation_url(user.email)
    try:
        await send_email(
            user.email,
            "Confirm your email",
            (
                f"Hello, {user.name}!\n\n"
                f"Confirm your email by clicking the link below: {confirmation_url}\n\n"
                f"If you did not create this account, please ignore this email.\n\n"
                f"Best regards,\n"
                f"{config.APP_NAME}"
            ),
            html=(
                f"<html>"
                f"<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>"
                f"<div style='max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;'>"
                f"<h2 style='color: #4A90E2;'>Hello, {user.name}!</h2>"
                f"<p>Thank you for signing up! Please confirm your email address to activate your account.</p>"
                f"<div style='margin: 30px 0;'>"
                f"<a href='{confirmation_url}' style='background-color: #4A90E2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;'>Confirm Email Address</a>"
                f"</div>"
                f"<p style='font-size: 0.9em; color: #666;'>If the button above doesn't work, copy and paste this link into your browser:</p>"
                f"<p style='font-size: 0.9em; color: #666;'>{confirmation_url}</p>"
                f"<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>"
                f"<p>If you did not create this account, please ignore this email.</p>"
                f"<p>Best regards,<br><strong>{config.APP_NAME} Team</strong></p>"
                f"</div>"
                f"</body>"
                f"</html>"
            ),
        )
    except MailResponseException as e:
        logger.error(f"Error sending email: {e}")


def send_password_reset_email(user: User, background_tasks: BackgroundTasks):
    background_tasks.add_task(_send_password_reset_email_task, user)


async def _send_password_reset_email_task(user: User):
    email = user.email
    reset_url = await create_password_reset_url(email)
    try:
        await send_email(
            email,
            "Resete sua senha",
            (
                f"Olá, {user.name}!\n\n"
                f"Você solicitou a recuperação de sua senha. Clique no link abaixo para criar uma nova senha:\n"
                f"{reset_url}\n\n"
                f"Este link expira em 15 minutos.\n\n"
                f"Se você não solicitou isso, por favor ignore este e-mail.\n\n"
                f"Atenciosamente,\n"
                f"{config.APP_NAME}"
            ),
            html=(
                f"<html>"
                f"<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>"
                f"<div style='max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;'>"
                f"<h2 style='color: #4A90E2;'>Olá, {user.name}!</h2>"
                f"<p>Você solicitou a recuperação de sua senha. Clique no botão abaixo para resetar sua senha:</p>"
                f"<div style='margin: 30px 0;'>"
                f"<a href='{reset_url}' style='background-color: #4A90E2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;'>Resetar Senha</a>"
                f"</div>"
                f"<p style='font-size: 0.9em; color: #666;'>Este link expira em 15 minutos.</p>"
                f"<p style='font-size: 0.9em; color: #666;'>Se o botão acima não funcionar, copie e cole este link no seu navegador:</p>"
                f"<p style='font-size: 0.9em; color: #666;'>{reset_url}</p>"
                f"<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>"
                f"<p>Se você não solicitou isso, por favor ignore este e-mail.</p>"
                f"<p>Atenciosamente,<br><strong>Equipe {config.APP_NAME}</strong></p>"
                f"</div>"
                f"</body>"
                f"</html>"
            ),
        )
    except MailResponseException as e:
        logger.error(f"Error sending password reset email: {e}")
