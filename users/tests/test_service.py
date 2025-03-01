import pytest
from unittest.mock import MagicMock, patch
from werkzeug.security import generate_password_hash
from app.service.user_service import UserService
from app.db.entity import UserEntity, ActivationTokenEntity
from app.service.dto import RegisterUserDto, UserDto
import datetime

@pytest.fixture
def mock_user_repository():
    """
    Fixture that creates a mock user repository for testing.

    This mock repository simulates a database interaction for user data,
    including methods for finding users by username or email.

    Returns:
        MagicMock: A mocked UserRepository object simulating a real repository.
    """
    return MagicMock()


@pytest.fixture
def mock_client_repository():
    """
    Fixture that creates a mock client repository for testing.

    This mock repository simulates a database interaction for client data,
    used in user management.

    Returns:
        MagicMock: A mocked ClientRepository object simulating a real repository.
    """
    return MagicMock()


@pytest.fixture
def mock_activation_token_repository():
    """
    Fixture that creates a mock activation token repository for testing.

    This mock repository simulates a database interaction for activation tokens,
    used to activate or verify user accounts.

    Returns:
        MagicMock: A mocked ActivationTokenRepository object simulating a real repository.
    """
    return MagicMock()


@pytest.fixture
def user_service(mock_user_repository, mock_client_repository, mock_activation_token_repository):
    """
    Fixture that creates a UserService instance for testing.

    This fixture initializes a UserService with mocked repositories and allows
    for testing user registration, activation, and related functionality.

    Args:
        mock_user_repository (MagicMock): Mocked user repository.
        mock_client_repository (MagicMock): Mocked client repository.
        mock_activation_token_repository (MagicMock): Mocked activation token repository.

    Returns:
        UserService: A UserService object ready for testing.
    """
    return UserService(mock_user_repository, mock_client_repository, mock_activation_token_repository)


def test_user_dto_to_client_entity():
    """
    Test case for converting UserDto to ClientEntity.

    This test verifies that a UserDto, when converted, properly creates
    a ClientEntity with the correct values from a UserEntity.

    Asserts:
        - First name matches.
        - Last name matches.
        - Email matches.
        - Phone number matches.
    """
    user_entity = UserEntity(
        id_=1,
        username="testuser",
        email="test@example.com",
        phone_number="123456789",
        first_name="Test",
        last_name="User",
        role="user"
    )
    user_dto = UserDto.from_user_entity(user_entity)

    client_entity = user_dto.to_client_entity(user_entity)

    assert client_entity.first_name == "Test"
    assert client_entity.last_name == "User"
    assert client_entity.email == "test@example.com"
    assert client_entity.phone_number == "123456789"


def test_register_user_success(user_service, mock_user_repository, mock_client_repository, mock_activation_token_repository):
    """
    Test case for successful user registration.

    This test simulates a successful user registration process, including
    validating the registration data and ensuring that the user's data
    is correctly stored and activation email is sent.

    Asserts:
        - The registered user's username and email match.
        - The email sending function is called once.
    """
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
    """
    Test case for user registration when the username already exists.

    This test simulates a scenario where a user tries to register with a
    username that already exists in the database. It should raise a ValueError.

    Asserts:
        - A ValueError is raised with the message "Username is already exists".
    """
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

    with pytest.raises(ValueError, match="Username already exists"):
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
    """
    Test case for user registration when the email already exists.

    This test simulates a scenario where a user tries to register with an
    email that already exists in the database. It should raise a ValueError.

    Asserts:
        - A ValueError is raised with the message "Username is already exists".
    """
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

    with pytest.raises(ValueError, match='Username already exists'):
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
    """
    Test case for successful user activation.

    This test simulates a successful user activation process where an activation
    token is validated and the user's account status is updated.

    Asserts:
        - The activated user's username and email match.
        - The user's `is_active` status is set to True.
    """
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
    """
    Test case for activating a user with an invalid token.

    This test simulates an attempt to activate a user with an invalid or non-existing
    activation token. It should raise a ValueError with the appropriate message.

    Asserts:
        - A ValueError is raised with the message "User not found".
    """
    mock_activation_token_repository.find_by_token.return_value = None

    with pytest.raises(ValueError, match="User not found"):
        user_service.activate_user("invalid_token")


def test_activate_user_expired_token(user_service, mock_activation_token_repository):
    """
    Test case for activating a user with an expired token.

    This test simulates an attempt to activate a user with an expired token.
    It should raise a ValueError with the message "Token has been expired".

    Asserts:
        - A ValueError is raised with the message "Token has been expired".
    """
    mock_activation_token = MagicMock()
    mock_activation_token.is_active.return_value = False
    mock_activation_token_repository.find_by_token.return_value = mock_activation_token

    with pytest.raises(ValueError, match="Token has expired"):
        user_service.activate_user("expired_token")

