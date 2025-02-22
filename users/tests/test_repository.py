import pytest
from unittest.mock import MagicMock, patch
from app.db.entity import UserEntity, ClientEntity, ActivationTokenEntity
from app.db.repository import UserRepository, ClientRepository, ActivationTokenRepository
from app.db.configuration import sa
from sqlalchemy.orm import joinedload


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def user_repo(mock_db):
    return UserRepository(mock_db)


@pytest.fixture
def client_repo(mock_db):
    return ClientRepository(mock_db)


@pytest.fixture
def activation_repo(mock_db):
    return ActivationTokenRepository(mock_db)


def test_save_or_update(user_repo):
    user = UserEntity(id_=1, username="testuser", email="test@example.com")

    user_repo.save_or_update(user)

    user_repo.sa.session.add.assert_called_once_with(user)
    user_repo.sa.session.commit.assert_called_once()


def test_find_by_id(user_repo):
    mock_user = UserEntity(id_=1, username="testuser", email="test@example.com")

    mock_query = MagicMock()
    mock_query.get.return_value = mock_user
    user_repo.sa.session.query.return_value = mock_query

    result = user_repo.find_by_id(1)

    assert result == mock_user
    user_repo.sa.session.query.assert_called_once_with(UserEntity)
    mock_query.get.assert_called_once_with(1)


def test_find_all(user_repo):
    mock_users = [UserEntity(id_=1, username="user1"), UserEntity(id_=2, username="user2")]

    mock_query = MagicMock()
    mock_query.all.return_value = mock_users
    user_repo.sa.session.query.return_value = mock_query

    result = user_repo.find_all()

    assert result == mock_users
    user_repo.sa.session.query.assert_called_once_with(UserEntity)
    mock_query.all.assert_called_once()


def test_delete_by_id(user_repo):
    mock_user = UserEntity(id_=1, username="testuser")

    user_repo.find_by_id = MagicMock(return_value=mock_user)

    user_repo.delete_by_id(1)

    user_repo.sa.session.delete.assert_called_once_with(mock_user)
    user_repo.sa.session.commit.assert_called_once()


def test_delete_all(user_repo):
    mock_query = MagicMock()
    user_repo.sa.session.query.return_value = mock_query

    user_repo.delete_all()

    mock_query.delete.assert_called_once()
    user_repo.sa.session.commit.assert_called_once()


def test_find_by_username(user_repo):
    mock_user = UserEntity(id_=1, username="testuser")

    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_user
    user_repo.sa.session.query.return_value = mock_query

    result = user_repo.find_by_username("testuser")

    assert result == mock_user
    user_repo.sa.session.query.assert_called_once_with(UserEntity)
    mock_query.filter_by.assert_called_once_with(username="testuser")


def test_find_by_email(user_repo):
    mock_user = UserEntity(id_=1, email="test@example.com")

    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_user
    user_repo.sa.session.query.return_value = mock_query

    result = user_repo.find_by_email("test@example.com")

    assert result == mock_user
    user_repo.sa.session.query.assert_called_once_with(UserEntity)
    mock_query.filter_by.assert_called_once_with(email="test@example.com")


def test_find_by_last_name(client_repo):
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
    mock_client = ClientEntity(id_=1, email="client@example.com")

    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = mock_client
    client_repo.sa.session.query.return_value = mock_query
    result = client_repo.find_by_email("client@example.com")

    assert result == mock_client
    client_repo.sa.session.query.assert_called_once_with(ClientEntity)
    mock_query.filter_by.assert_called_once_with(email="client@example.com")





