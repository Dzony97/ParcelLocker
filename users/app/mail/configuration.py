from flask import Flask
from flask_mail import Mail, Message


class MailSender:
    """
    Class responsible for sending emails using Flask-Mail.

    Attributes:
        _mail (Mail): The Mail object responsible for sending the email.
        _sender (str): The email address used as the sender for outgoing emails.

    Methods:
        __init__(app: Flask, sender: str) -> None: Initializes the MailSender with Flask app and sender's email address.
        send(email: str, subject: str, content: str) -> None: Sends an email with the specified recipient, subject, and content.
    """

    _mail = None
    _sender = None

    def __init__(self, app: Flask, sender: str) -> None:
        """
        Initializes the MailSender with Flask app and sender's email address.

        Args:
            app (Flask): The Flask application to configure Flask-Mail with.
            sender (str): The email address used as the sender for outgoing emails.
        """
        MailSender._mail = Mail(app)
        MailSender._sender = sender

    @classmethod
    def send(cls, email: str, subject: str, content: str) -> None:
        """
        Sends an email with the specified recipient, subject, and content.

        Args:
            email (str): The recipient's email address.
            subject (str): The subject of the email.
            content (str): The HTML content of the email.
        """
        mail_content = f'''
            <html>
                <body>
                    <div style="font-family:Consolas;margin:auto 100px;padding:5px;text-size:16px;color:white;background-color:grey">
                        {content}
                    </div>
                </body>
            </html>
        '''
        message = Message(
            subject=subject,
            sender=cls._sender,
            recipients=[email],
            html=mail_content
        )

        cls._mail.send(message)
