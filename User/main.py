from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from dependencies import get_db, templates, env
from User import models, schemas, utils
from sqlalchemy.orm import Session
from User import OAuth2
import re


router = APIRouter()



@router.get("/")
def registration(request: Request, db: Session = Depends(get_db)):
    template = env.get_template("registration.html")
    return templates.TemplateResponse(template, {"request": request})


@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    template = env.get_template("registration.html")
    errors = []
    first_name = form.get('first_name')
    last_name = form.get('last_name')
    email = form.get('email')
    phone_number = form.get('phone_number')
    password = form.get('password')
    cnf_password = form.get('cnf_password')

    if utils.validation.name(first_name) and utils.validation.name(last_name):
        errors.append("Length of Names should be greater than 3")
    if utils.validation.phone_validation(phone_number):
        errors.append("Phone Number is not Correct!!!")
    if utils.validation.email_validation(email):
        errors.append("Email is not valid!!!")
    if utils.validation.password_check(password, cnf_password):
        errors.append("Password is not same or less than 6 characters !!!")

    if len(errors) > 0:
        return templates.TemplateResponse(template, {"request": request, "errors": errors})

    password = utils.hash_password(password)
    new_user = models.User(first_name=first_name, last_name=last_name,
                           email=email, phone_number=phone_number, password=password)
    try:
        db.add(new_user)
        db.commit()
    except:
        return templates.TemplateResponse(template, {"request": request, "msg": "Email or Phone is already registered!!!"})
    return templates.TemplateResponse(template, {"request": request, "msg": "Successfully Registered, Kindly Login..."})





@router.post('/login')
def signin(request: Request, response: Response, userdata: OAuth2PasswordRequestForm = Depends(),
           db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == userdata.username)
    template = env.get_template("registration.html")
    errors = []
    if user_query.first() is None:
        errors.append("Not Registered !!!")
        return templates.TemplateResponse(template, {"request": request, "errors": errors})
    user = user_query.first()
    if not utils.verify_password(userdata.password, user.password):
        errors.append("Credentials are incorrect !!!")
        return templates.TemplateResponse(template, {"request": request, "errors": errors})
    print(user.first_name)
    access_token = OAuth2.create_access_token(data={"user_id": user.id})
    response = RedirectResponse(url="/product", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f'Bearer {access_token}', httponly=True)
    return response


@router.get("/logout")
def signout(request: Request, response: Response, db: Session = Depends(get_db)):
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response
