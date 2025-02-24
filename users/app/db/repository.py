from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from app.db.entity import ClientEntity, UserEntity, ActivationTokenEntity
from app.db.configuration import sa
import logging

logging.basicConfig(level=logging.INFO)


class CrudRepository[T](ABC):

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

    def __init__(self, db: SQLAlchemy) -> None:
        self.sa = db
        self.entity_type = self.__class__.__orig_bases__[0].__args__[0]

    def save_or_update(self, entity: T) -> None:
        self.sa.session.add(entity)
        self.sa.session.commit()

    def save_or_update_many(self, entities: list[T]) -> None:
        self.sa.session.add_all(entities)
        self.sa.session.commit()

    def find_by_id(self, entity_id: int) -> T | None:
        return self.sa.session.query(self.entity_type).get(entity_id)

    def find_all(self) -> list[T]:
        return self.sa.session.query(self.entity_type).all()

    def delete_by_id(self, entity_id: int) -> None:
        entity = self.find_by_id(entity_id)
        if entity:
            self.sa.session.delete(entity)
            self.sa.session.commit()

    def delete_all(self) -> None:
        self.sa.session.query(self.entity_type).delete()
        self.sa.session.commit()


class UserRepository(CrudRepositoryORM[UserEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    def find_by_username(self, username: str) -> UserEntity | None:
        return self.sa.session.query(UserEntity).filter_by(username=username).first()

    def find_by_email(self, email: str) -> UserEntity | None:
        return self.sa.session.query(UserEntity).filter_by(email=email).first()


class ClientRepository(CrudRepositoryORM[ClientEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    def find_by_last_name(self, last_name: str) -> list[ClientEntity]:
        return self.sa.session.query(ClientEntity).filter_by(last_name=last_name).all()

    def find_by_email(self, email: str) -> ClientEntity | None:
        return self.sa.session.query(ClientEntity).filter_by(email=email).first()


class ActivationTokenRepository(CrudRepositoryORM[ActivationTokenEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db)

    @staticmethod
    def find_by_token(token: str) -> ActivationTokenEntity | None:
        return ActivationTokenEntity.query.options(joinedload(ActivationTokenEntity.user)).filter_by(
            token=token).first()


user_repository = UserRepository(sa)
client_repository = ClientRepository(sa)
activation_token_repository = ActivationTokenRepository(sa)
