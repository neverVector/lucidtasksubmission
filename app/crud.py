from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts_by_user(db: Session, user_id: int):
    return db.query(models.Post).filter(models.Post.owner_id == user_id).all()

def delete_post(db: Session, post_id: int, user_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == user_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False