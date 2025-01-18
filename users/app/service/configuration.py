from app.service.user_service import UserService
from app.db.repository import user_repository, client_repository

user_service = UserService(user_repository, client_repository)