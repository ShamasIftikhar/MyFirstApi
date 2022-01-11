from fastapi.testclient import TestClient
from app.database import get_db, Base
import pytest
from app.main import app
from app.config import setting
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionlocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture(scope="module")
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @pytest.fixture(scope="module")
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)
