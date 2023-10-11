import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or "you-will-never-guess"
