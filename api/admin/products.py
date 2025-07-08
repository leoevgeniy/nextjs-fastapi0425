from sqladmin import Admin, ModelView
from api.models.settings import Settings
from api.models.product import Promos


class PromosAdmin(ModelView, model=Promos):
    column_list = [Promos.endDate, Promos.title]
    column_sortable_list = [Promos.endDate]
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    
    