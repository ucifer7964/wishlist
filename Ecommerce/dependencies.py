from starlette.templating import Jinja2Templates
from database import SessionLocal
from jinja2 import FileSystemLoader, Environment
import stripe

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


loader = FileSystemLoader([
    "templates/",
    "shop/templates",
    "cart/templates",
    "orders/templates",
    "payment/templates",
    "admin/templates",
    "User/templates"
])

env = Environment(loader=loader)
templates = Jinja2Templates(directory="templates")
stripe.api_key = "sk_test_51Kj8lvSInkdhZrgnNfKwypIhEj1zMixSjOcpTdqu1p7rd1JbFABJZQy4ouagB4ZPp4JcPnYmFoF25SSWvakXCJ6R000ovlSL0p"
