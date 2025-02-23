import pytest
from unittest.mock import MagicMock, patch
from werkzeug.security import generate_password_hash
from app.service.user_service import UserService
from app.db.entity import UserEntity, ActivationTokenEntity
from app.service.dto import RegisterUserDto, UserDto
import datetime

@pytest.fixture
def mock_user_repository():
    return MagicMock()

@pytest.fixture
def mock_client_repository():
    return MagicMock()

@pytest.fixture
def mock_activation_token_repository():
    return MagicMock()

@pytest.fixture
def user_service(mock_user_repository, mock_client_repository, mock_activation_token_repository):
    return UserService(mock_user_repository, mock_client_repository, mock_activation_token_repository)


def test_register_user_success(user_service, mock_user_repository, mock_client_repository, mock_activation_token_repository):
    register_dto = RegisterUserDto(
        username="testuser",
        email="test@example.com",
        password="password",
        password_confirmation="password",
        phone_number="123456789",
        first_name="Test",
        last_name="User",
        role="user"
    )
    user_dto = UserDto(
        id_=1,
        username="testuser",
        email="test@example.com",
        phone_number="123456789",
        first_name="Test",
        last_name="User",
        role="user"
    )

    register_dto.check_passwords = MagicMock(return_value=True)
    register_dto.with_password = MagicMock(return_value=register_dto)
    register_dto.to_user_entity = MagicMock(return_value=UserEntity(id_=1, username="testuser", email="test@example.com"))

    mock_user_repository.find_by_username.return_value = None
    mock_user_repository.find_by_email.return_value = None

    with patch("app.service.user_service.MailSender.send") as mock_mail_sender:
        result = user_service.register_user(register_dto, user_dto)
        assert result["username"] == "testuser"
        assert result["email"] == "test@example.com"
        mock_mail_sender.assert_called_once()


def test_register_user_username_exists(user_service, mock_user_repository):
    register_dto = RegisterUserDto(
        username="testuser",
        email="test@example.com",
        password="password",
        password_confirmation="password",
        phone_number="123456789",
        first_name="Test",
        last_name="User",
        role="user"
    )
    mock_user_repository.find_by_username.return_value = True

    with pytest.raises(ValueError, match="Username is already exists"):
        user_service.register_user(register_dto, UserDto(
            id_=1,
            username="testuser",
            email="test@example.com",
            phone_number="123456789",
            first_name="Test",
            last_name="User",
            role="user"
        ))


def test_register_user_email_exists(user_service, mock_user_repository):
    register_dto = RegisterUserDto(
        username="testuser",
        email="test@example.com",
        password="password",
        password_confirmation="password",
        phone_number="123456789",
        first_name="Test",
        last_name="User",
        role="user"
    )
    mock_user_repository.find_by_email.return_value = True

    with pytest.raises(ValueError, match='Username is already exists'):
        user_service.register_user(register_dto, UserDto(
            id_=1,
            username="testuser",
            email="test@example.com",
            phone_number="123456789",
            first_name="Test",
            last_name="User",
            role="user"
        ))


def test_activate_user_success(user_service, mock_activation_token_repository, mock_user_repository):
    token = "valid_token"
    mock_activation_token = MagicMock()
    mock_activation_token.is_active.return_value = True
    mock_activation_token.user = MagicMock(id_=1, username="testuser", email="test@example.com", is_active=False)

    mock_activation_token_repository.find_by_token.return_value = mock_activation_token
    result = user_service.activate_user(token)

    assert result["username"] == "testuser"
    assert result["email"] == "test@example.com"
    assert mock_activation_token.user.is_active is True


def test_activate_user_invalid_token(user_service, mock_activation_token_repository):
    mock_activation_token_repository.find_by_token.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        user_service.activate_user("invalid_token")


def test_activate_user_expired_token(user_service, mock_activation_token_repository):
    mock_activation_token = MagicMock()
    mock_activation_token.is_active.return_value = False
    mock_activation_token_repository.find_by_token.return_value = mock_activation_token

    with pytest.raises(ValueError, match="Token has been expired"):
        user_service.activate_user("expired_token")
