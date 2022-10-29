from server import server_intialize
import sys
import pytest
from dotenv import load_dotenv
# sys.path.append('../../Data-Explorer-BackEnd/server.py')


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture
def client():
    SERVER = server_intialize()
    with SERVER.test_client() as client:
        yield client