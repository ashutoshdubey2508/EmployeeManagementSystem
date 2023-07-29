from rest_framework import serializers
from employee.models import Admin, Employee_model 
 

class Adminserializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['name','email','password'] 
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()       

        return instance

 
class EmployeeSerializer(serializers.ModelSerializer):
    manager_id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Employee_model
        fields = ['name', 'email', 'contact_number', 'blood_group', 'Father_name', 'physically_challenged', 'Religion',
                  'Graduation', 'percentage', 'passing_year', 'address', 'department', 'designation', 'location',
                  'password', 'manager_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # def create(self, validated_data):
    #     manager_id = validated_data.pop('manager_id', None)
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)

    #     if password is not None:
    #         instance.set_password(password)

    #     if manager_id is not None:
    #         instance.manager = Employee_model.objects.filter(id=manager_id).first()

    #     instance.save()
    #     return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.id  # Include the 'id' field in the response
        return data