import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
FRONTEND_DIST = os.path.join(PROJECT_DIR, "frontend", "dist")


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(DATA_DIR, "pharma_qms.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "pharma-qms-standalone"

    static_folder = os.path.join(FRONTEND_DIST, "static")
    template_folder = FRONTEND_DIST
