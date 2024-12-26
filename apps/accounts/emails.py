""" accounts email functions"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_register_welcome(
    user,
    action_url: str,
):
    """Send a welcome  e-mail message to new user"""
    subject = f"Bem-vindo(a) ao {settings.APPLICATION_NAME}"
    list_emails = [
        user.email,
    ]

    html_content = render_to_string(
        "emails/register-welcome.html",
        {
            "user": user,
            "action_url": action_url,
            "login_url": settings.APPLICATION_FRONTEND_LOGIN_URL,
            "project_name": settings.APPLICATION_NAME,
            "company_address": settings.COMPANY_ADDRESS,
            "support_email": settings.APPLICATION_SUPPORT_EMAIL,
            "project_website": settings.APPLICATION_FRONTEND_URL,
        },
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=settings.EMAIL_HOST_USER, to=list_emails
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_password_reset(user, email: str, project_name: str, company_address: str, action_url: str):
    subject = "TasKing - Definir Palavra-passe"
    list_emails = [
        email,
    ]

    html_content = render_to_string(
        "emails/password-reset.html",
        {"user": user, "project_name": project_name, "company_address": company_address, "action_url": action_url},
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject, body=text_content, from_email=settings.EMAIL_HOST_USER, to=list_emails
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
