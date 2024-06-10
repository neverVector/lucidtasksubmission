from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud, auth, dependencies
from cachetools import cached, TTLCache

router = APIRouter()

cache = TTLCache(maxsize=100, ttl=300)  # Caches data for 5 minutes

@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=email)
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/addpost", response_model=schemas.Post)
def add_post(
    post: schemas.PostCreate,
    token: str = Depends(auth.oauth2_scheme),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(dependencies.get_current_active_user)
):
    if len(post.text.encode('utf-8')) > 1048576:
        raise HTTPException(status_code=400, detail="Payload too large")
    return crud.create_post(db=db, post=post, user_id=current_user.id)

@cached(cache)
@router.get("/getposts", response_model=List[schemas.Post])
def get_posts(
    token: str = Depends(auth.oauth2_scheme),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(dependencies.get_current_active_user)
):
    return crud.get_posts_by_user(db, user_id=current_user.id)

@router.delete("/deletepost")
def delete_post(
    post_id: int,
    token: str = Depends(auth.oauth2_scheme),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(dependencies.get_current_active_user)
):
    success = crud.delete_post(db=db, post_id=post_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post successfully deleted"}