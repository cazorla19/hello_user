import json

def test_hello(client):
    response = client.get('/')
    json_data = json.loads(response.data)
    assert json_data['hello'] == 'world'
