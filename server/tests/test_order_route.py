from fastapi.testclient import TestClient
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app

client = TestClient(app)

def test_get_order_valid_token():
    # create new user
    data = {"email": "user1@test.com", "username": "test", "password": "test"}
    client.post("/users/register", json.dumps(data))
    # get access token
    data = {"email": "user1@test.com", "password": "test"}
    response = client.post("/users/login", json.dumps(data))
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.get("/orders", headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_get_order_invalid_token():
    # create new user
    data = {"email": "user2@test.com", "username": "test", "password": "test"}
    client.post("/users/register", json.dumps(data))
    # get access token
    data = {"email": "user2@test.com", "password": "test"}
    response = client.post("/users/login", json.dumps(data))
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.get("/orders", headers={'Authorization': f'Bearer {token+"random"}'})
    assert response.status_code == 403 #should fail -- invalid token


def test_post_order():
    # create new user
    data = {"email": "user3@test.com", "username": "test", "password": "test"}
    client.post("/users/register", json.dumps(data))
    # get access token
    data = {"email": "user3@test.com", "password": "test"}
    response = client.post("/users/login", json.dumps(data))
    assert response.status_code == 200
    token = response.json()["access_token"]

    no_orders_before_post = len(client.get("/orders", headers={'Authorization': f'Bearer {token}'}).json())

    data = {
        "plates": [
            {
                "plate_id": 1,
                "quantity": 420
            },
            {
                "plate_id": 2,
                "quantity": 42
            }
        ]
    }

    response = client.post("/orders", json.dumps(data) ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    no_orders_after_post = len(client.get("/orders", headers={'Authorization': f'Bearer {token}'}).json())
    assert no_orders_before_post + 1 == no_orders_after_post  # number of orders incremented by one
