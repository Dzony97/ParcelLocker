import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from flask_mail import Message
from app.mail.configuration import MailSender


@pytest.fixture
def app():
    """
    Fixture to create and configure a Flask application instance for testing.

    The application is configured with testing settings, including mock SMTP configurations
    that simulate the real email settings for sending emails.

    Yields:
        Flask: A Flask application instance configured for testing email sending.
    """
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["MAIL_SERVER"] = "smtp.example.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "test@example.com"
    app.config["MAIL_PASSWORD"] = "password"
    return app


@pytest.fixture
def mail_sender(app):
    """
    Fixture to create an instance of the MailSender class for sending emails.

    This fixture sets up the `MailSender` with the Flask app instance and the sender email.

    Args:
        app (Flask): The Flask application instance to be used for sending emails.

    Returns:
        MailSender: The MailSender instance used for email sending.
    """
    return MailSender(app, sender="no-reply@example.com")


def test_send_email(mail_sender):
    """
    Test for the send method in the MailSender class.

    This test checks that the email is correctly constructed and that the send method
    is called with the expected parameters when sending an email.

    Args:
        mail_sender (MailSender): The MailSender instance used to send the email.
    """
    with patch.object(mail_sender._mail, 'send') as mock_send:
        # Call the send method to simulate sending an email.
        mail_sender.send("user@example.com", "Test Subject", "Test Content")

        # Ensure that the send method was called once.
        mock_send.assert_called_once()

        # Retrieve the sent message from the call arguments.
        sent_message = mock_send.call_args[0][0]

        # Assertions to verify that the email was constructed properly.
        assert isinstance(sent_message, Message)  # Ensure the message is of type Message
        assert sent_message.subject == "Test Subject"  # Verify the subject
        assert sent_message.sender == "no-reply@example.com"  # Verify the sender email
        assert sent_message.recipients == ["user@example.com"]  # Verify the recipient
        assert "Test Content" in sent_message.html  # Verify the content is in the HTML body of the message
