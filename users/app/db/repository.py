from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from app.db.entity import ClientEntity, UserEntity, ActivationTokenEntity
from app.db.configuration import sa
import logging

logging.basicConfig(level=logging.INFO)


class CrudRepository[T](ABC):
    """
    Abstract base class for CRUD operations on entities.

    Methods:
        save_or_update(entity: T) -> None: Saves or updates the provided entity.
        save_or_update_many(entities: list[T]) -> None: Saves or updates multiple entities.
        find_by_id(entity_id: int) -> T | None: Retrieves an entity by its ID.
        find_all() -> list[T]: Retrieves all entities of the type.
        delete_by_id(entity_id: int) -> None: Deletes an entity by its ID.
        delete_all() -> None: Deletes all entities of the type.
    """

    @abstractmethod
    def save_or_update(self, entity: T) -> None:
        pass

    @abstractmethod
    def save_or_update_many(self, entities: list[T]) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> T | None:
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass


class CrudRepositoryORM[T: sa.Model](CrudRepository[T]):
    """
    Concrete implementation of the CrudRepository interface, utilizing SQLAlchemy for ORM functionality.

    Methods:
        save_or_update(entity: T) -> None: Saves or updates a given entity in the database.
        save_or_update_many(entities: list[T]) -> None: Saves or updates multiple entities in the database.
        find_by_id(entity_id: int) -> T | None: Retrieves an entity by its ID from the database.
        find_all() -> list[T]: Retrieves all entities of the type from the database.
        delete_by_id(entity_id: int) -> None: Deletes an entity by its ID from the database.
        delete_all() -> None: Deletes all entities of the type from the database.
    """

    def __init__(self, db: SQLAlchemy) -> None:
        self.sa = db
        self.entity_type = self.__class__.__orig_bases__[0].__args__[0]

    def save_or_update(self, entity: T) -> None:
        """
        Saves or updates the given entity in the database.

        Args:
            entity (T): The entity to save or update.
        """
        self.sa.session.add(entity)
        self.sa.session.commit()

    def save_or_update_many(self, entities: list[T]) -> None:
        """
        Saves or updates multiple entities in the database.

        Args:
            entities (list[T]): A list of entities to save or update.
        """
        self.sa.session.add_all(entities)
        self.sa.session.commit()

    def find_by_id(self, entity_id: int) -> T | None:
        """
        Retrieves an entity by its ID.

        Args:
            entity_id (int): The ID of the entity to retrieve.

        Returns:
            T | None: The entity if found, otherwise None.
        """
        return self.sa.session.query(self.entity_type).get(entity_id)

    def find_all(self) -> list[T]:
        """
        Retrieves all entities of the type.

        Returns:
            list[T]: A list of all entities of the type.
        """
        return self.sa.session.query(self.entity_type).all()

    def delete_by_id(self, entity_id: int) -> None:
        """
        Deletes an entity by its ID.

        Args:
            entity_id (int): The ID of the entity to delete.
        """
        entity = self.find_by_id(entity_id)
        if entity:
            self.sa.session.delete(entity)
            self.sa.session.commit()

    def delete_all(self) -> None:
        """
        Deletes all entities of the type.
        """
        self.sa.session.query(self.entity_type).delete()
        self.sa.session.commit()


class UserRepository(CrudRepositoryORM[UserEntity]):
    """
    Repository for performing CRUD operations on UserEntity.

    Methods:
        find_by_username(username: str) -> UserEntity | None: Retrieves a user by username.
        find_by_email(email: str) -> UserEntity | None: Retrieves a user by email.
    """

    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    def find_by_username(self, username: str) -> UserEntity | None:
        """
        Retrieves a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            UserEntity | None: The user if found, otherwise None.
        """
        return self.sa.session.query(UserEntity).filter_by(username=username).first()

    def find_by_email(self, email: str) -> UserEntity | None:
        """
        Retrieves a user by their email.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            UserEntity | None: The user if found, otherwise None.
        """
        return self.sa.session.query(UserEntity).filter_by(email=email).first()


class ClientRepository(CrudRepositoryORM[ClientEntity]):
    """
    Repository for performing CRUD operations on ClientEntity.

    Methods:
        find_by_last_name(last_name: str) -> list[ClientEntity]: Retrieves a list of clients by last name.
        find_by_email(email: str) -> ClientEntity | None: Retrieves a client by email.
    """

    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    def find_by_last_name(self, last_name: str) -> list[ClientEntity]:
        """
        Retrieves a list of clients by their last name.

        Args:
            last_name (str): The last name of the clients to retrieve.

        Returns:
            list[ClientEntity]: A list of clients with the matching last name.
        """
        return self.sa.session.query(ClientEntity).filter_by(last_name=last_name).all()

    def find_by_email(self, email: str) -> ClientEntity | None:
        """
        Retrieves a client by their email.

        Args:
            email (str): The email of the client to retrieve.

        Returns:
            ClientEntity | None: The client if found, otherwise None.
        """
        return self.sa.session.query(ClientEntity).filter_by(email=email).first()


class ActivationTokenRepository(CrudRepositoryORM[ActivationTokenEntity]):
    """
    Repository for performing CRUD operations on ActivationTokenEntity.

    Methods:
        find_by_token(token: str) -> ActivationTokenEntity | None: Retrieves an activation token by its value.
    """

    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    @staticmethod
    def find_by_token(token: str) -> ActivationTokenEntity | None:
        """
        Retrieves an activation token by its value.

        Args:
            token (str): The token value to search for.

        Returns:
            ActivationTokenEntity | None: The activation token if found, otherwise None.
        """
        return ActivationTokenEntity.query.options(joinedload(ActivationTokenEntity.user)).filter_by(
            token=token).first()


user_repository = UserRepository(sa)
client_repository = ClientRepository(sa)
activation_token_repository = ActivationTokenRepository(sa)
