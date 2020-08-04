import os
from typing import List
from requests import post, Response


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:
    FROM_TITLE = 'Pricing Service'
    FROM_EMAIL = 'simon@sandbox09afaee962f84bcc8b521c466c7ab377.mailgun.org'

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)
        if api_key is None:
            raise MailgunException('Failed to load Mailgun APIkey')

        if domain is None:
            raise MailgunException('Failed to load Mailgun Domain')

        response = post(
            f"{domain}/messages",
            auth=("api", api_key),
            data={"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html})
        if response.status_code != 200:
            print(response.status_code)
            print(response.json())
            raise MailgunException('An error has occurred while sending the email!')
        return response
