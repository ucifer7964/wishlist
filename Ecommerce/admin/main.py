from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from dependencies import get_db
from admin import schemas
from shop import models
from dependencies import env, templates

router = APIRouter()


@router.get("/admin")
def dashboard(request: Request):
    template = env.get_template('dashboard.html')
    return templates.TemplateResponse(template, {'request': request})


@router.post("/create")
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/create/{id}")
def update_product(id: int, product: schemas.Product, db: Session = Depends(get_db)):
    new_product = db.query(models.Product).filter(models.Product.id == id)
    if new_product.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
    new_product.update(product.dict(), synchronize_session=False)
    db.commit()
    return new_product.first()
