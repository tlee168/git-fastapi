
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# the following line create the tables for you if tables are missing
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins=["*"] #every single origin

origins = [
    "https://www.google.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my fastapi"}

# my_posts = [
#     {"title": "title of post 1",
#      "content": "content of post 1",
#      "id": 1
#     },
#     {"title": "title of post 2",
#      "content": "content of post 2",
#      "id": 2
#     }
# ]



# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data:": posts}



