from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import jwt, datetime
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from .serializers import EmployeeSerializer,ManagerSerializer
from .models import Employee_model,Manager_model

# REGISTEREMP

class RegisterManagerView(APIView):
    def post(self, request):
        serializer =  ManagerSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# LOGINMANAGER 

class LoginManagerView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']

        manager = Manager_model.objects.filter(email=email).first()

        if manager is None:
            raise AuthenticationFailed("Manager Not found")
        
        if not manager.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        payload = {
            'id' : manager.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes= 60),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm = 'HS256')

        
        response =Response()

        response.set_cookie(key='jwt',value = token , httponly = True)

        response.data={
            'jwt' : token
        }

        return response

#get managerinformation

class  GetManagerInfo(APIView):
    def get(self , request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token , 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')

        manager = Manager_model.objects.filter(id = payload['id']).first()


        serializer = ManagerSerializer(manager)

        return Response(serializer.data)     

# manager logout

class ManagerLogoutView(APIView):
    def post(self ,request):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Already logged out')

        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : 'success'
        }        

        return response
    

# ADDEMP

class EmpAddView(APIView):
    def post(self , request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token , 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        employee_check = Employee_model.objects.filter(email = request.data['email']).first()

        if employee_check is not None:
            raise AuthenticationFailed('employee already present')

        manager = Manager_model.objects.filter(id = payload['id']).first()

        employee = Employee_model.objects.create(
            emp_name=request.data['emp_name'],
            email=request.data['email'],
            password=request.data['password'],
            team_name=request.data['team_name'],
            manager_details=manager
        )
        
        # employee = Employee_model()
        
        # employee.objects.create(emp_name = request.data['emp_name'] ,email = request.data['email'], password = request.data['password'] , team_name = request.data['team_name'], manager_details = manager )

        # employee.save()

        serializer = EmployeeSerializer(employee)

        return Response(serializer.data)


#deleteEmployee


class EmpDeleteView(APIView):
    def post(self ,request):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')
        
        try:
            payload = jwt.decode(token , 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        employee_delete = request.data['email']

        manager = Manager_model.objects.filter(id = payload['id']).first()

        employee=Employee_model.objects.filter(email = employee_delete,manager_details = manager).first()

        if not employee:
            raise AuthenticationFailed("Employee not found")
        
        employee.delete()

        response = Response()
        
        response.data = {
            "message" : "success"
        }

        return response


#GETemployeedata


class GetEmployeeView(APIView):
    def get(self ,request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token , 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        employee_mail = request.data['email']

        if not employee_mail:
            raise AuthenticationFailed("employee not found")
        
        result = Employee_model.objects.get(email = employee_mail)

        serializer = EmployeeSerializer(result)

        return Response(serializer.data)
    
#update Employeedata

class UpdateEmployeeView(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token , 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        

        employee_mail = request.data['email']

        if not employee_mail:
            raise AuthenticationFailed('Incorrect mail')
        
        try:
            employee = Employee_model.objects.get(email=request.data['email'])
        except Employee_model.DoesNotExist:
            raise Http404('Employee not found.')

        employee.emp_name = request.data['emp_name']
        employee.email = request.data['email']
        employee.password = request.data['password']
        employee.team_name = request.data['team_name']


        serializer = EmployeeSerializer(instance=employee, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            raise AuthenticationFailed('Invalid data')    

        response = Response()

        response.data = {
            "message" : "success"
        }

        return response
    

#GETAllemployee 

class GetAnyEmployee(APIView):
    def get(self ,request):
        employee_mail = request.data['email']

        if not employee_mail:
            raise AuthenticationFailed("employee not found")
        
        result = Employee_model.objects.get(email = employee_mail)

        serializer = EmployeeSerializer(result)

        return Response(serializer.data)
    

#GETall_loggedinemployee

class GetAllLoggedInEmployee(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token , 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        manager = Manager_model.objects.filter(id = payload['id']).first()

        if not manager:
            raise AuthenticationFailed('manager not found')

        employee = Employee_model.objects.filter(manager_details = manager)

        serializer = EmployeeSerializer(employee , many = True)

        return Response(serializer.data)

class Displayallemp(APIView):
    
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('unauthenticated')

        try:
            payload = jwt.decode(token , 'secret' , algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        empobj = Employee_model.objects.all()

        serializer = EmployeeSerializer(empobj, many=True)

        return Response(serializer.data)
            

               

