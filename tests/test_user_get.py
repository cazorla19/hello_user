import json
from datetime import datetime, date

HEADERS = {'content-type': 'application/json'}

def test_valid_status_code(client):
    user = "vanrossum"
    request_data = {"dateOfBirth": "1956-01-31"}
    client.put('/hello/%s' % user, data=json.dumps(request_data), headers=HEADERS)
    response = client.get('/hello/%s' % user)
    assert response.status_code == 200

def test_valid_message(client):
    user = "torvalds"
    request_data = {"dateOfBirth": "1969-12-28"}

    # Calculate the actual days number
    today_date = date.today()
    bday = request_data["dateOfBirth"]
    bday_date = datetime.strptime(bday, "%Y-%m-%d").date().replace(year=today_date.year)
    # Set the birthday up to the next year if it's already gone at this one
    if bday_date < today_date:
        bday_date = bday_date.replace(year=today_date.year+1)
    diff = bday_date - today_date

    client.put('/hello/%s' % user, data=json.dumps(request_data), headers=HEADERS)
    response = client.get('/hello/%s' % user)
    json_data = json.loads(response.data)

    assert json_data["message"] == "Hello, %s! Your birthday is in %s day(s)" % (user, diff.days)

def test_valid_today_message(client):
    user = "luckyguy"
    today_date = date.today().strftime("%Y-%m-%d")
    request_data = {"dateOfBirth": today_date}

    client.put('/hello/%s' % user, data=json.dumps(request_data), headers=HEADERS)
    response = client.get('/hello/%s' % user)
    json_data = json.loads(response.data)

    assert json_data["message"] == "Hello, %s! Happy birthday!" % user
