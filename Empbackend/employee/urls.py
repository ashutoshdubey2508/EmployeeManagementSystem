from django.urls import path
from .views import RegisterManagerView, LoginManagerView , GetManagerInfo , ManagerLogoutView , EmpAddView , EmpDeleteView, GetEmployeeView, UpdateEmployeeView, GetAnyEmployee, GetAllLoggedInEmployee, Displayallemp

urlpatterns = [
   
    path('register_manager/', RegisterManagerView.as_view(), name='manager-registration'),
    path('login_manager/',LoginManagerView.as_view()),
    path('get_manager/', GetManagerInfo.as_view()),
    path('logout_manager/', ManagerLogoutView.as_view()),
    path('add_employee/',EmpAddView.as_view()),
    path('delete_employee/',EmpDeleteView.as_view()),
    path('get_employee/',GetEmployeeView.as_view()),
    path('update_employee/',UpdateEmployeeView.as_view()),
    path('getany_employee/',GetAnyEmployee.as_view()),
    path('getallloggedin_employee/',GetAllLoggedInEmployee.as_view()),
    path('display_all/',Displayallemp.as_view())
]