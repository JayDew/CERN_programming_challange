from fastapi.testclient import TestClient
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app

client = TestClient(app)

def test_user_can_leave_a_review_to_an_ordered_dish():
    # create new user
    data = {"email": "user4@test.com", "username": "test", "password": "test"}
    client.post("/users/register", json.dumps(data))
    # get access token
    data = {"email": "user4@test.com", "password": "test"}
    response = client.post("/users/login", json.dumps(data))
    assert response.status_code == 200
    token = response.json()["access_token"]

    # place order
    data_order = {
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

    response = client.post("/orders", json.dumps(data_order) ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    # leave review
    data_review = {
        "plate_id": 1,
        "review": "Best food ever",
        "rating": 5
    }
    response = client.post("/review/add", json.dumps(data_review) ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    # # the average rating of the dish should be 5
    response = client.get("/review/1/average" ,headers={'Authorization': f'Bearer {token}'})
    assert response.json() == 5


def test_user_cannot_leave_a_review_to_an_not_ordered_dish():
    # create new user
    data = {"email": "user5@test.com", "username": "test", "password": "test"}
    client.post("/users/register", json.dumps(data))
    # get access token
    data = {"email": "user5@test.com", "password": "test"}
    response = client.post("/users/login", json.dumps(data))
    assert response.status_code == 200
    token = response.json()["access_token"]

    # place order
    data_order = {
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

    response = client.post("/orders", json.dumps(data_order) ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    # leave review
    data_review = {
        "plate_id": 3,
        "review": "Should fail",
        "rating": 5
    }
    response = client.post("/review/add", json.dumps(data_review) ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404

def test_user_cannot_leave_multiple_reviews():
    # create new user
    data = {"email": "user6@test.com", "username": "test", "password": "test"}
    client.post("/users/register", json.dumps(data))
    # get access token
    data = {"email": "user6@test.com", "password": "test"}
    response = client.post("/users/login", json.dumps(data))
    assert response.status_code == 200
    token = response.json()["access_token"]

    # place order
    data_order = {
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

    response = client.post("/orders", json.dumps(data_order) ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    # leave review #1
    data_review = {
        "plate_id": 1,
        "review": "Should work",
        "rating": 5
    }
    response = client.post("/review/add", json.dumps(data_review) ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    # leave review #2
    data_review = {
        "plate_id": 1,
        "review": "Should NOT work",
        "rating": 5
    }
    response = client.post("/review/add", json.dumps(data_review) ,headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
