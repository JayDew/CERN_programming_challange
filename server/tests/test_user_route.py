from fastapi.testclient import TestClient
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app

client = TestClient(app)

def test_create_user():
    data = {"email": "user@test.com", "username": "test", "password": "test"}
    response = client.post("/users/register", json.dumps(data))
    assert response.status_code == 200


def test_cannot_create_user_twice():
    data = {"email": "user@test.com", "username": "test2", "password": "test2"}
    response = client.post("/users/register", json.dumps(data))
    assert response.status_code == 400


def test_invalid_email_address():
    data = {"email": "not_valid", "username": "test2", "password": "test2"}
    response = client.post("/users/register", json.dumps(data))
    assert response.status_code == 422


def test_login_successful():
    data = {"email": "user@test.com", "password": "test"}
    response = client.post("/users/login", json.dumps(data))
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None  # token exists


def test_login_fail():
    data = {"email": "not@working.com", "password": "test"}
    response = client.post("/users/login", json.dumps(data))
    assert response.status_code == 400