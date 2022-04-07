from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    url: str
    available: bool
    price: int
    slug: str
    category_id: str

    class Meta:
        load_instance = True
