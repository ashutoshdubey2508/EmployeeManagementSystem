from django.contrib import admin
from .models import Employee_model,Admin

class AdminEmployee_model(admin.ModelAdmin):
    pass
    
admin.site.register(Employee_model, AdminEmployee_model)
admin.site.register(Admin, AdminEmployee_model)


