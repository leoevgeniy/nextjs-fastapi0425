from api.DAO.base import BaseDAO
from api.models.settings import Settings


class SettingsDAO(BaseDAO):
    model = Settings