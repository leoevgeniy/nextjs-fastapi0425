from fastapi import APIRouter, Depends
from api.database.database import async_session
from api.DAO.settings import SettingsDAO


router = APIRouter(
    prefix="/api/settings",
    tags=["Settings"]
)


@router.get("/get_settings")
async def get_settings():
    settings = await SettingsDAO.find_one_or_none(is_active=True)
    print(settings.company_logo)
    return settings
