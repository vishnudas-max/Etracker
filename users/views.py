from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .Serializers import UserRegistrationSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

User = get_user_model

#for setting up csrf token cookie on the frontend
@method_decorator(ensure_csrf_cookie,name='dispatch')
class CsrfTokenView(APIView):
    def get(self,request):
        return JsonResponse({'message':'csrf cookie set'})

#view to handle user registration
class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User Registerd Succesfully.'},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#view to handle user login
class LoginView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
        
        if not username or not password:
            return Response({'message':'Username and Password are required !'},status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request,username=username,password=password)     
        if user is not None:
            login(request,user)
            return Response({'message':'login success full'},status=status.HTTP_200_OK)
        else:
            return Response({'message':'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)

#to logout the user
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


#for checking user is authenticated 
class CheckAuthView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self,request):
        if request.user.is_authenticated:
            return Response({
                'is_authenticated':True,
                'user':{
                    'id':request.user.id,
                    'username':request.user.username
                }
            })
        else:
            return Response({
                'is_authenticated':False
            })