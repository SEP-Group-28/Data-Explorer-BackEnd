import pytest
from dotenv import load_dotenv
import app

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture
def client():
    APP = app.create_app()
    with APP.test_client() as client:
        yield client
