import json

HEADERS = {'content-type': 'application/json'}

def test_valid_data(client):
    user = "johndoe"
    request_data = {"dateOfBirth": "1970-01-01"}
    response = client.put('/hello/%s' % user, data=json.dumps(request_data), headers=HEADERS)
    assert response.status_code == 204

def test_invalid_username(client):
    users = ["johndoe1970", "1970", "john_doe", "john-doe", "[johndoe]", "*johndoe*"]
    request_data = {"dateOfBirth": "1970-01-01"}
    status_code_set = set()
    for user in users:
        response = client.put('/hello/%s' % user, data=json.dumps(request_data), headers=HEADERS)
        status_code_set.add(response.status_code)
    accepted_status_codes = [400]
    # Check if all request errors are within accepted status codes list
    assert status_code_set.intersection(set(accepted_status_codes)) == status_code_set

def test_nonexistent_field(client):
    user = "sartre"
    request_data = {"dateOfBird": "1905-06-21"}
    response = client.put('/hello/%s' % user, data=json.dumps(request_data), headers=HEADERS)
    assert response.status_code == 400

# We will just pass data as a key/value dict, not as JSON
def test_invalid_data_type(client):
    user = "dostoevsky"
    request_data = {"dateOfBirth": "1821-11-11"}
    response = client.put('/hello/%s' % user, data=request_data, headers=HEADERS)
    assert response.status_code == 400

# I hope no one will use this test after 2215 year
def test_invalid_bday(client):
    user = "mcfly"
    request_data = {"dateOfBirth": "2215-01-01"}
    response = client.put('/hello/%s' % user, data=json.dumps(request_data), headers=HEADERS)
    assert response.status_code == 400
