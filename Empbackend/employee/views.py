from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import jwt, datetime
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from .serializers import EmployeeSerializer, Adminserializer
from .models import Employee_model, Admin
from django.contrib.auth.hashers import check_password
from .Deco import jwt_auth_required


class RegisterEmployeeView(APIView):
    def post(self, request):
        data = request.data
        employee_check = Employee_model.objects.filter(email=data['email']).first()

        if employee_check is not None:
            raise AuthenticationFailed('employee already present')

        manager_id = data.get('manager_id')  
       
        employee = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password'],
            'contact_number': data['contact_number'],
            'blood_group': data['blood_group'],
            'Father_name': data['Father_name'],
            'physically_challenged': data['physically_challenged'],
            'Religion': data['Religion'],
            'Graduation': data['Graduation'],
            'percentage': data['percentage'],
            'passing_year': data['passing_year'],
            'address': data['address'],
            'department': data['department'],
            'designation': data['designation'],
            'location': data['location'],
            'image': data['image'],
            'manager_id': manager_id  
        }

        serializer = EmployeeSerializer(data=employee)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# LOGINMANAGER 

class LoginManagerView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        manager = Employee_model.objects.filter(email=email).first()
        # query_set = Employee_model.objects.filter(manager=manager.subemployee)
        # print(manager.subemployee.all())
        # print(manager.manager.name)

        if manager is None:
            raise AuthenticationFailed("Employee Not found")
        
        if not password == manager.password:
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


class LoginAdminView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        manager = Admin.objects.filter(email=email).first()
      
        if manager is None:
            raise AuthenticationFailed("Admin Not found")
        
        if not password==manager.password:
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



#logout
class EmployeeLogoutView(APIView):
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

# #get managerinformation

class  GetEmployeeInfo(APIView):
    def get(self , request , employee_id):

        employee = Employee_model.objects.filter(id = employee_id).first()


        serializer = EmployeeSerializer(employee)

        return Response(serializer.data)    


class GetonlyManagerView(APIView):
    # @jwt_auth_required
    def get(self, request):
        token = request.headers["Authorization"].split("Bearer ")[1]
        decode_token = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = decode_token['id']
        manager = Employee_model.objects.filter(id=user_id).first()

        if not manager:
            return Response({'error': 'Manager not found'}, status=404)

        serializer = EmployeeSerializer(manager)
        
        return Response({'user_id': user_id, 'manager_data': serializer.data})
  

# # manager logout

class Reporting_to(APIView):
    def get(self, request , manager_id):
        
        employee = Employee_model.objects.filter(id=manager_id).first()

        manager = employee.manager
        

        if not manager:
            return Response({'error': 'Employee not found'}, status=404)

        serializer = EmployeeSerializer(manager)
        return Response(serializer.data) 
    
class MyteamView(APIView):
    def get(self,request , current_id):
        employee = Employee_model.objects.filter(id = current_id).first()
        if not employee:
            raise AuthenticationFailed('wrong id entered')
        return_data = employee.subemployee.all()
        if not return_data:
            raise AuthenticationFailed('Does not have team')

        serializer = EmployeeSerializer(return_data , many = True)

        return Response(serializer.data)         

# # ADDEMP

class EmpAddView(APIView):
    def post(self , request):
        data = request.data
        
        employee_check = Employee_model.objects.filter(email=request.data['email']).first()

        if employee_check is not None:
            raise AuthenticationFailed('employee already present')

        manager_id = data.get('manager_id')  

        employee = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password'],
            'contact_number': data['contact_number'],
            'blood_group': data['blood_group'],
            'Father_name': data['Father_name'],
            'physically_challenged': data['physically_challenged'],
            'Religion': data['Religion'],
            'Graduation': data['Graduation'],
            'percentage': data['percentage'],
            'passing_year': data['passing_year'],
            'address': data['address'],
            'department': data['department'],
            'designation': data['designation'],
            'location': data['location'],
            'image': data['image'],
            'manager_id': manager_id  
        }

        serializer = EmployeeSerializer(data=employee)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# #deleteEmployee


class EmpDeleteView(APIView):
    def delete(self ,request , id ):

        employee=Employee_model.objects.filter(id = id).first()

        if not employee:
            raise AuthenticationFailed("Employee not found")
        
        employee.delete()

        response = Response()
        
        response.data = {
            "message" : "success"
        }

        return response

    
# #update Employeedata

class UpdateEmployeeView(APIView):
    def put(self, request):
        data=request.data

        employee_mail = request.data['email']

        if not employee_mail:
            raise AuthenticationFailed('Incorrect mail')
        
        try:
            employee = Employee_model.objects.get(email=request.data['email'])
        except Employee_model.DoesNotExist:
            raise Http404('Employee not found.')
        
        employee.name = data['name']
        employee.email= data['email']
        employee.contact_number=data['contact_number']
        employee.blood_group = data['blood_group']
        employee.Father_name = data['Father_name']
        employee.physically_challenged = data['physically_challenged']
        employee.Religion = data['Religion']
        employee.Graduation = data['Graduation']
        employee.percentage = data['percentage']
        employee.passing_year = data['passing_year']
        employee.address = data['address']
        employee.department =  data['department']
        employee.designation = data['designation']
        employee.location = data['location']
        employee.image = data['image']
        employee.manager_id = data['manager_id']


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
    

class Getall(APIView):
    def get(self, request):
        data = Employee_model.objects.all()
        serializer = EmployeeSerializer(data , many = True)
        return Response(serializer.data)
               

