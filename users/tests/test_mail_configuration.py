import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from flask_mail import Message
from app.mail.configuration import MailSender


@pytest.fixture
def app():
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
    return MailSender(app, sender="no-reply@example.com")


def test_send_email(mail_sender):
    with patch.object(mail_sender._mail, 'send') as mock_send:
        mail_sender.send("user@example.com", "Test Subject", "Test Content")

        mock_send.assert_called_once()
        sent_message = mock_send.call_args[0][0]

        assert isinstance(sent_message, Message)
        assert sent_message.subject == "Test Subject"
        assert sent_message.sender == "no-reply@example.com"
        assert sent_message.recipients == ["user@example.com"]
        assert "Test Content" in sent_message.html
