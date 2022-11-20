import sys
import pytest
sys.path.append('./')
import server 

@pytest.fixture  #TESTING INTIALIZER
def client():
    SERVER = server.server_intialize()
    with SERVER.test_client() as client:
        yield client
