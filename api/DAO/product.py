from api.DAO.base import BaseDAO
from api.models.product import Catalog, Product, Promos


class ProductDAO(BaseDAO):
    model = Product
    
class CatalogDAO(BaseDAO):
    model = Catalog
    
class PromosDAO(BaseDAO):
    model = Promos