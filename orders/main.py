from fastapi import APIRouter, Request, Depends, Form, status, BackgroundTasks
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from cart.cart import Cart
from dependencies import get_db, templates, env
from orders import crud
from payment.crud import payment_process
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from orders import schemas
from config import settings
from orders.models import Order, OrderItem
from User import OAuth2, utils

router = APIRouter(
    prefix="/order"
)


# This method will fetch the checkout page
@router.get("/create_order")
def order_add(request: Request, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    cart = Cart(request, db)
    template = env.get_template('order.html')

    return templates.TemplateResponse(template, {"request": request,
                                                 "cart": cart})


# This method will save the details regarding order and create the order
@router.post("/create_order")
async def order_add(request: Request, db: Session = Depends(get_db),
                    current_user: int = Depends(OAuth2.get_current_user)):
    # extracting data
    form = await request.form()
    first_name = form.get('first_name')
    last_name = form.get('last_name')
    email = form.get('email')
    address = form.get('address')
    postal_code = form.get('postal_code')
    city = form.get('city')

    cart = Cart(request, db)
    template = env.get_template('order.html')
    errors = []
    # validating the data with help of validation class
    if utils.validation.name(first_name) or utils.validation.name(last_name):
        errors.append("Length of Names should be greater than 3 ")
    if utils.validation.name(address) or utils.validation.name(city):
        errors.append("Address should be more descriptive !")
    if utils.validation.email_validation(email):
        errors.append("Email is not valid!!!")
    if utils.validation.postal_code(str(postal_code)):
        errors.append("Invalid Postal Code!!!")

    if len(errors) > 0:
        return templates.TemplateResponse(template, {"request": request, "errors": errors, "cart": cart})

    total_price = cart.get_total_price_after_discount()

    db_order = crud.create_order(db, first_name, last_name, email, address, postal_code,
                                 city, coupon_id=cart.coupon_id, discount=cart.get_discount(), total_price=total_price,
                                 user_id=current_user.id)
    order_id = db_order.id
    request.session["order_id"] = order_id

    request.session["total_price"] = total_price
    payment_session = payment_process(total_price)

    # Here we are storing the data related to each product regarding an order.
    for item in cart:
        product_id = item["product"]["id"]
        crud.create_order_item(item, order_id, product_id, db)

    cart.remove_all()
    return RedirectResponse(url=payment_session.url, status_code=status.HTTP_303_SEE_OTHER)


conf = ConnectionConfig(
    MAIL_USERNAME=f"{settings.mail_username}",
    MAIL_PASSWORD=f"{settings.mail_password}",
    MAIL_FROM=f"{settings.mail_from}",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


# This method will send the mail in the format provided in Mail.html  to given email
@router.post("/send_mail")
async def send_with_template(request: Request, db: Session = Depends(get_db),
                             current_user: int = Depends(OAuth2.get_current_user)):
    order_id = request.session.get('order_id')
    order_detail = db.query(Order).filter_by(id=order_id).first()
    customer_email = order_detail.email
    template_body = {
        "first_name": order_detail.first_name,
        "last_name": order_detail.last_name,
        "address": order_detail.address,
        "postal_code": order_detail.postal_code,
        "city": order_detail.city,
        "date": order_detail.created_date,
        "bill": request.session.get("total_price")
    }
    message = MessageSchema(
        subject="Shopping List from WishList",
        recipients=[customer_email],  # List of recipients, as many as you can pass
        template_body=template_body
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="Mail.html")
    return RedirectResponse(url="/product", status_code=status.HTTP_303_SEE_OTHER)
