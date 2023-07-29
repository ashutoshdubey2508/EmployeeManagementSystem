from django.urls import path
from .views import RegisterEmployeeView , LoginManagerView, GetEmployeeInfo, Reporting_to, MyteamView ,EmpAddView ,UpdateEmployeeView,EmpDeleteView,LoginAdminView ,GetonlyManagerView, Getall  

urlpatterns = [
   
    path('register_employee/', RegisterEmployeeView.as_view(), name='manager-registration'),
    path('login_employee/',LoginManagerView.as_view()),
    path('login_admin/',LoginAdminView.as_view()),
    path('getonly_manager/',GetonlyManagerView.as_view()),
    path('get_employee/<int:employee_id>', GetEmployeeInfo.as_view()),
    path('get_manager/<int:manager_id>',Reporting_to.as_view()),
    path('get_myteam/<int:current_id>', MyteamView.as_view()),
    path('add_employee/',EmpAddView.as_view()),
    path('delete_employee/<int:id>',EmpDeleteView.as_view()),
    path('update_employee/',UpdateEmployeeView.as_view()),
    path('get_all/',Getall.as_view())
]