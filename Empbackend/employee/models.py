from django.db import models
import uuid 
from django.contrib.auth.models import AbstractBaseUser
# from .employee_model import Employee_model

class Admin(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','email','password']


class Employee_model(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    contact_number = models.IntegerField()
    blood_group = models.TextField(max_length=3)
    Father_name = models.CharField(max_length=255)
    physically_challenged = models.CharField(max_length=3)
    Religion = models.CharField(max_length=255)
    Graduation = models.CharField(max_length=255)
    percentage = models.IntegerField()
    passing_year = models.IntegerField()
    address = models.TextField()
    department = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    location = models.TextField()
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)
    manager = models.ForeignKey('Employee_model', on_delete=models.SET_NULL, null=True, blank=True,related_name='subemployee')  # manager_id is employee_id of manager
    username = None
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [ 'name','email','password'] 

