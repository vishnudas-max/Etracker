from rest_framework import serializers
from .models import Expense
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['username']
            read_only_fields = ['username']
            
class ExpenseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Expense
        fields = ['id','title','amount','category','date','notes','user']
        
