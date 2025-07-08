from api.DAO.base import BaseDAO
from api.models.user import User


class UserDAO(BaseDAO):
    model = User