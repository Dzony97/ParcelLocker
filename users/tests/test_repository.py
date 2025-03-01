import pytest
from unittest.mock import MagicMock, patch
from app.db.entity import UserEntity, ClientEntity, ActivationTokenEntity
from app.db.repository import UserRepository, ClientRepository, ActivationTokenRepository
from app.db.configuration import sa
from sqlalchemy.orm import joinedload


@pytest.fixture
def mock_db():
    """
    Fixture to mock the database session for testing purposes.

    This mock is used to simulate interactions with the database
    without making actual database calls.

    Yields:
        MagicMock: A mocked database session.
    """
    return MagicMock()


@pytest.fixture
def user_repo(mock_db):
    """
    Fixture to create a UserRepository instance with a mocked database session.

    This fixture is used for testing methods in the UserRepository class.

    Args:
        mock_db (MagicMock): A mocked database session.

    Returns:
        UserRepository: The UserRepository instance configured for testing.
    """
    return UserRepository(mock_db)


@pytest.fixture
def client_repo(mock_db):
    """
    Fixture to create a ClientRepository instance with a mocked database session.

    This fixture is used for testing methods in the ClientRepository class.

    Args:
        mock_db (MagicMock): A mocked database session.

    Returns:
        ClientRepository: The ClientRepository instance configured for testing.
    """
    return ClientRepository(mock_db)


@pytest.fixture
def activation_repo(mock_db):
    """
    Fixture to create an ActivationTokenRepository instance with a mocked database session.

    This fixture is used for testing methods in the ActivationTokenRepository class.

    Args:
        mock_db (MagicMock): A mocked database session.

    Returns:
        ActivationTokenRepository: The ActivationTokenRepository instance configured for testing.
    """
    return ActivationTokenRepository(mock_db)


def test_save_or_update(user_repo):
    """
    Test for the save_or_update method in the UserRepository class.

    This test checks that a user entity is added to the session and committed properly.

    Args:
        user_repo (UserRepository): The UserRepository instance used to test the save_or_update method.
    """
    user = UserEntity(id_=1, username="testuser", email="test@example.com")

    user_repo.save_or_update(user)

    user_repo.sa.session.add.assert_called_once_with(user)
    user_repo.sa.session.commit.assert_called_once()


def test_find_by_id(user_repo):
    """
    Test for the find_by_id method in the UserRepository class.

    This test ensures that the method correctly queries a user by their ID.

    Args:
        user_repo (UserRepository): The UserRepository instance used to test the find_by_id method.
    """
    mock_user = UserEntity(id_=1, username="testuser", email="test@example.com")

    mock_query = MagicMock()
    mock_query.get.return_value = mock_user
    user_repo.sa.session.query.return_value = mock_query

    result = user_repo.find_by_id(1)

    assert result == mock_user
    user_repo.sa.session.query.assert_called_once_with(UserEntity)
    mock_query.get.assert_called_once_with(1)


def test_find_all(user_repo):
    """
    Test for the find_all method in the UserRepository class.

    This test ensures that the method returns all users from the database.

    Args:
        user_repo (UserRepository): The UserRepository instance used to test the find_all method.
    """
    mock_users = [UserEntity(id_=1, username="user1"), UserEntity(id_=2, username="user2")]

    mock_query = MagicMock()
    mock_query.all.return_value = mock_users
    user_repo.sa.session.query.return_value = mock_query

    result = user_repo.find_all()

    assert result == mock_users
    user_repo.sa.session.query.assert_called_once_with(UserEntity)
    mock_query.all.assert_called_once()


def test_delete_by_id(user_repo):
    """
    Test for the delete_by_id method in the UserRepository class.

    This test ensures that a user is deleted by their ID and the changes are committed.

    Args:
        user_repo (UserRepository): The UserRepository instance used to test the delete_by_id method.
    """
    mock_user = UserEntity(id_=1, username="testuser")

    user_repo.find_by_id = MagicMock(return_value=mock_user)

    user_repo.delete_by_id(1)

    user_repo.sa.session.delete.assert_called_once_with(mock_user)
    user_repo.sa.session.commit.assert_called_once()


def test_delete_all(user_repo):
    """
    Test for the delete_all method in the UserRepository class.

    This test ensures that all users are deleted and the changes are committed.

    Args:
        user_repo (UserRepository): The UserRepository instance used to test the delete_all method.
    """
    mock_query = MagicMock()
    user_repo.sa.session.query.return_value = mock_query

    user_repo.delete_all()

    mock_query.delete.assert_called_once()
    user_repo.sa.session.commit.assert_called_once()


def test_find_by_username(user_repo):
    """
    Test for the find_by_username method in the UserRepository class.

    This test checks that a user can be retrieved by their username.

    Args:
        user_repo (UserRepository): The UserRepository instance used to test the find_by_username method.
    """
    mock_user = UserEntity(id_=1, username="testuser")

    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_user
    user_repo.sa.session.query.return_value = mock_query

    result = user_repo.find_by_username("testuser")

    assert result == mock_user
    user_repo.sa.session.query.assert_called_once_with(UserEntity)
    mock_query.filter_by.assert_called_once_with(username="testuser")


def test_find_by_email(user_repo):
    """
    Test for the find_by_email method in the UserRepository class.

    This test checks that a user can be retrieved by their email.

    Args:
        user_repo (UserRepository): The UserRepository instance used to test the find_by_email method.
    """
    mock_user = UserEntity(id_=1, email="test@example.com")

    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_user
    user_repo.sa.session.query.return_value = mock_query

    result = user_repo.find_by_email("test@example.com")

    assert result == mock_user
    user_repo.sa.session.query.assert_called_once_with(UserEntity)
    mock_query.filter_by.assert_called_once_with(email="test@example.com")


def test_find_by_last_name(client_repo):
    """
    Test for the find_by_last_name method in the ClientRepository class.

    This test checks that clients can be retrieved by their last name.

    Args:
        client_repo (ClientRepository): The ClientRepository instance used to test the find_by_last_name method.
    """
    mock_clients = [ClientEntity(id_=1, last_name="Doe")]

    mock_query = MagicMock()
    mock_query.filter_by.return_value.all.return_value = mock_clients
    client_repo.sa.session.query.return_value = mock_query

    result = client_repo.find_by_last_name("Doe")

    assert result == mock_clients
    client_repo.sa.session.query.assert_called_once_with(ClientEntity)
    mock_query.filter_by.assert_called_once_with(last_name="Doe")
    mock_query.filter_by.return_value.all.assert_called_once()


def test_find_by_email_client(client_repo):
    """
    Test for the find_by_email method in the ClientRepository class.

    This test checks that a client can be retrieved by their email.

    Args:
        client_repo (ClientRepository): The ClientRepository instance used to test the find_by_email method.
    """
    mock_client = ClientEntity(id_=1, email="client@example.com")

    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_client
    client_repo.sa.session.query.return_value = mock_query
    result = client_repo.find_by_email("client@example.com")

    assert result == mock_client
    client_repo.sa.session.query.assert_called_once_with(ClientEntity)
    mock_query.filter_by.assert_called_once_with(email="client@example.com")
