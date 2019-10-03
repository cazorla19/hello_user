import pytest
from hello_user import api

@pytest.fixture
def client():
    client = api.APP.test_client()
    return client
