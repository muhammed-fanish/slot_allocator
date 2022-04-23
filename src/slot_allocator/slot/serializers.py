from rest_framework import serializers
from .models import UserSlot
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegister(serializers.ModelSerializer) :
    password2 = serializers.CharField(style={'input_type' : 'password'})
    is_hr = serializers.CharField(style={'input_type' : 'text'})


    class Meta:
        model = User
        fields = ['username','email','password','password2','is_hr']


    def save(self) :
        reg = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            is_superuser=self.validated_data['is_hr']
            
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        is_hr=self.validated_data['is_hr']

        if password !=password2 :
            raise serializers.ValidationError({"password" :"Password does not match"})

        if int(is_hr) not in[1,0] :
            raise serializers.ValidationError({"is_hr" :"is_hr must be 0 or 1 "})


        reg.set_password(password)
        reg.save()
        return reg


class UserSlot(serializers.ModelSerializer) :
    class Meta:
        model = UserSlot
        fields = ['user_id','slot_date','from_time','to_time']

    def save(self) :
        user = User.objects.get(id=)
        reg = UserSlot(
            user=user,
            slot_date=self.validated_data['slot_date'],
            form_time=self.validated_data['form_time'],
            to_time=self.validated_data['to_time']
        )
        reg.save()
        return reg


