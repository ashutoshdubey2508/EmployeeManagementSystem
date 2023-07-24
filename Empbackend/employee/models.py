from django.db import models
import uuid 
from django.contrib.auth.models import AbstractBaseUser
# from .employee_model import Employee_model

class Manager_model(AbstractBaseUser):
    manager_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['manager_name','email','password']


class Employee_model(AbstractBaseUser):
    emp_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    manager_details = models.ForeignKey( Manager_model, on_delete=models.CASCADE)
    username = None

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [ 'emp_name','email','password','manger_id'] 

