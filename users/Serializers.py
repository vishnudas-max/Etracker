from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required =True,style={'input_type':'password'})
    password2 = serializers.CharField(write_only=True, required = True,style={'input_type':'password'})
    email = serializers.EmailField(required =True)
    
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs={
            'password':{'write_only':True},
            'password2': {'write_only':True},
        }
        
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password":"Passwords does not match!"})
    
        try:
            validate_password(data['password'],user=User(username=data['username']))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password":list(e.messages)})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with that username already exists."})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with that email already exists."})

        return data
    
    
    def create(self,validated_data):
        print(validated_data)
        validated_data.pop('password2')
        print(validated_data)
        user = User.objects.create_user(
            username= validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        
        return user

