import bcrypt
from sqladmin import Admin, ModelView

from api.auth.auth import get_password_hash
from api.models.user import User
class UserAdmin(ModelView, model=User):
    column_list = [User.email, User.phone]
    column_searchable_list = [User.email, User.phone]
    column_sortable_list = [User.registered_at]
    column_details_exclude_list = [User.password]
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    async def on_model_change(self, form, model, is_created, request):

        if form['password']:
            form['password'] = get_password_hash(form['password'])
        return await super().on_model_change(form, model, is_created, request)
        
        
