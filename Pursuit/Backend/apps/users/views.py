from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import RegisterSerializer , LoginSerializer , UserSerializer , ChangePassSerializer
from .models import User
# Create your views here.
#users views 
class SignUpAPI(generics.CreateAPIView):
    queryset = User.objects.all() 
    serializer_class = RegisterSerializer
    permission_classes= [permissions.AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        print(serializer.data)
        return Response({
        "user":{
    
"id":serializer.data.get("id"),    "full_name":serializer.data.get("full_name"),
    "email":serializer.data.get("email")
        } ,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=201)
 
 
class LoginAPI(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({
              "user":user_data,
              "refresh": str(refresh),
              "access": str(refresh.access_token),
              "message":"Login Successfully"
        },status = status.HTTP_200_OK)
      
        return Response(
           serializer.errors,
           status = status.HTTP_400_BAD_REQUEST
            )   
            
 
class LogOutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data["refresh"])
            token.blacklist()
            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError:
            return Response(
                {"message": "Token is invalid or already blacklisted"},
                status=status.HTTP_400_BAD_REQUEST,
            )   
    
    
class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
        

class ProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
           
class ChangePassAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = ChangePassSerializer(
        data =request.data,
        context={"request":request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_pass"])
            user.save()
            return Response({"message":"password changed successfully"},status = status.HTTP_200_OK)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST) 
        
        
        
        
    