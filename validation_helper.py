from enum import Enum
from pydantic import BaseModel

class Category(str, Enum):
    SALES = "SALES"
    PRODUCT = "PRODUCT"
    CUSTOMER = "CUSTOMER"

class ClassificationResult(BaseModel):
    category: Category
