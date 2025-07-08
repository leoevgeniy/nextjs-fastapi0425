from sqladmin import Admin, ModelView
from fastapi import FastAPI, UploadFile
from fastapi_storages import FileSystemStorage
from api.DAO.settings import SettingsDAO
from api.auth.auth import get_password_hash
from api.models.settings import Settings

def create_upload_file(file: UploadFile):
    FileSystemStorage(path="static").write(file)

class SettingsAdmin(ModelView, model=Settings):
    column_list = [Settings.is_active, Settings.company_name, Settings.company_phone]
    column_searchable_list = [Settings.company_name]
    column_sortable_list = [Settings.created_at]
    column_details_exclude_list = [Settings.company_email_password]
    page_size = 50
    page_size_options = [25, 50, 100, 200]

        
    async def on_model_change(self, form, model, is_created, request):
        all_settings = await SettingsDAO.find_all(is_active=True)
        for setting in all_settings:
            if setting.id != model.id and form['is_active']:
                await SettingsDAO.update_by_id(setting.id, {'is_active': False})
        if not form['is_active'] and model.id != 1:
            await SettingsDAO.update_by_id(1, {'is_active': True})
        elif not form['is_active'] and model.id == 1:
            form['is_active'] = True
        print(form)
        # if form['company_logo'] and Settings.company_logo != form['company_logo']:
        #     form['company_logo'] = Settings.company_logo
        # if form['company_email_password']:
        #     form['company_email_password'] = get_password_hash(form['company_email_password'])
        return await super().on_model_change(form, model, is_created, request)