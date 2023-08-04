import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_user(client, user):
    response = client.post("/api/register_employee/", user)
    assert response.data["name"] == user["name"]

@pytest.mark.django_db
def test_login_user(client, user):
    response = client.post("/api/register_employee/", user)
    response1 = client.post("/api/login_employee/", user)
    assert response1.data["email"] == user["email"]
    assert 'jwt' in response1.cookies

@pytest.mark.django_db
def test_login_user_incorrect_password(client, user):
    payload2 = {
         "name": "test",
        "email": "test@test.com",
        "password": "test1",
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
    response = client.post("/api/register_employee/", user)
    response2 = client.post("/api/login_employee/", payload2)
    assert response2.data["detail"] == "Incorrect password"

@pytest.mark.django_db
def test_logout_user(client, user):
    response = client.post("/api/register_employee/", user)
    response1 = client.post("/api/login_employee/", user)
    response2 = client.post("/api/logout_employee/", user)
    assert 'jwt' not in response2.cookies  

@pytest.mark.django_db
def test_get_user(client, user):
    response = client.post("/api/register_employee/", user)

    response1 = client.post("/api/login_employee/", user)
   

    employee_id = response1.data['id']  
    response2 = client.get(f"/api/get_employee/{employee_id}")  
    assert response2.data['email'] == user['email']
    assert response2.status_code == 200

    response3 = client.get(f"/api/get_employee/{employee_id+1}")
    assert response3.data["detail"] == "Employee not found"


@pytest.mark.django_db
def test_reportingto_user(client, user):
    response = client.post("/api/register_employee/", user)
    assert response.status_code == 201

    response1 = client.post("/api/login_employee/", user)
    assert response1.status_code == 200

    employee_id = response1.data['id']

    assert response1.data["email"] == user["email"]

    payload = {
        "name": "testing",
        "email": "testing@testing.com",
        "password": "testing",
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
        "manager_id": employee_id 
    }

    response3 = client.post("/api/register_employee/", payload)
    assert response3.status_code == 201
    assert response3.data["name"] == payload["name"]

    response4 = client.post("/api/login_employee/", payload)

    employee_id2 = response4.data['id']

   

    response5 = client.get(f"/api/get_manager/{employee_id2}")  

    assert response5.data['email'] == user['email']
    assert response5.status_code == 200


@pytest.mark.django_db
def test_getmyteam_user(client, user):
    response = client.post("/api/register_employee/", user)
    assert response.status_code == 201

    response1 = client.post("/api/login_employee/", user)
    assert response1.status_code == 200

    employee_id = response1.data['id']

    assert response1.data["email"] == user["email"]

    payload = {
        "name": "testing",
        "email": "testing@testing.com",
        "password": "testing",
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
        "manager_id": employee_id 
    }

    response3 = client.post("/api/register_employee/", payload)
    assert response3.status_code == 201
    assert response3.data["name"] == payload["name"]

    response4 = client.post("/api/login_employee/", payload)

    employee_id2 = response4.data['id']

   

    response5 = client.get(f"/api/get_myteam/{employee_id}")  

    assert len(response5.data) > 0
    assert response5.status_code == 200    

    response6 = client.get(f"/api/get_myteam/{employee_id+1000}")

    assert response6.data['detail'] == "wrong id entered"



@pytest.mark.django_db
def test_addemployee_user(client, user):
    response = client.post("/api/register_employee/", user)
    assert response.status_code == 201

    response1 = client.post("/api/login_employee/", user)
    assert response1.status_code == 200

    employee_id = response1.data['id']

    assert response1.data["email"] == user["email"]

    payload = {
        "name": "testing",
        "email": "testing@testing.com",
        "password": "testing",
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
        "manager_id": employee_id 
    }

    response3 = client.post("/api/add_employee/", payload)
    assert response3.status_code == 201
    assert response3.data["data"]["name"] == payload["name"]



@pytest.mark.django_db
def test_deleteemployee_user(client, user):
    response = client.post("/api/register_employee/", user)
    assert response.status_code == 201

    response1 = client.post("/api/login_employee/", user)
    assert response1.status_code == 200

    employee_id = response1.data['id']

    assert response1.data["email"] == user["email"]

    payload = {
        "name": "testing",
        "email": "testing@testing.com",
        "password": "testing",
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
        "manager_id": employee_id 
    }
     
    response3 = client.post("/api/add_employee/", payload)
    assert response3.status_code == 201
    assert response3.data["data"]["name"] == payload["name"]


    response = client.delete(f"/api/delete_employee/{employee_id}")
    assert response.data["message"] == "success"
    
    response = client.delete(f"/api/delete_employee/{employee_id+1000}")
    assert response.data["detail"] == "Employee not found"

@pytest.mark.django_db
def test_updateemployee_user(client, user):
    response = client.post("/api/register_employee/", user)
    assert response.status_code == 201

    response1 = client.post("/api/login_employee/", user)
    assert response1.status_code == 200

    employee_id = response1.data['id']

    assert response1.data["email"] == user["email"]

    payload = {
        "name": "testing",
        "email": "testing@testing.com",
        "password": "testing",
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
     
    response3 = client.put("/api/update_employee/", payload)
    assert response3.status_code == 404
    # assert response3.data["data"]["name"] == payload["name"]


    # response = client.delete(f"/api/delete_employee/{employee_id}")
    # assert response.data["message"] == "success"
    
    # response = client.delete(f"/api/delete_employee/{employee_id+1000}")
    # assert response.data["detail"] == "Employee not found"    



@pytest.mark.django_db
def test_getallemployee_user(client, user):
    response = client.post("/api/register_employee/", user)
    assert response.status_code == 201

    response1 = client.post("/api/login_employee/", user)
    assert response1.status_code == 200

    employee_id = response1.data['id']

    assert response1.data["email"] == user["email"]

    payload = {
        "name": "testing",
        "email": "testing@testing.com",
        "password": "testing",
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
        "manager_id" : employee_id
    }
    response = client.post("/api/add_employee/", payload)
    assert response.status_code == 201

    response3 = client.put("/api/get_all/")
    assert response3.status_code == 405
         



   