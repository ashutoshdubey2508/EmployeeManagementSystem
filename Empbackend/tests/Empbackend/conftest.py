import pytest
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user():
    return {
        "name": "test",
        "email": "test@test.com",
        "password": "test",
        "contact_number": "123456789",
        "blood_group": "B+",
        "Father_name": "fa",
        "physically_challenged": "NO",
        "Religion": "hindu",
        "Graduation": "B.tech",
        "percentage": 89,
        "passing_year": 2023,
        "address": "pune",
        "image": "",
        "department": "engineering",
        "designation": "senior manager",
        "location": "pune",
    }