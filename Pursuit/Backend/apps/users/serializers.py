from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
# users serializer
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','full_name','email','password']
    def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
   

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)
    def validate(self,data):
        email  = data["email"]
        password = data["password"]
        user = authenticate(
        username= email,
        password = password
        )
        if user is None:
            raise serializers.ValidationError("Invalid Credential")
        data["user"] = user
        return data
         
class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="full_name")
    class Meta:
        model = User
        fields = ['id','fullName','email']
        
 
class ChangePassSerializer(serializers.Serializer):
    current_pass = serializers.CharField(write_only =True)
    new_pass = serializers.CharField(write_only =True)
    re_enter_pass = serializers.CharField(write_only =True)
    def validate(self,data):
        user  = self.context['request'].user
        
        if not  user.check_password(data["current_pass"]):
            raise serializers.ValidationError({"current_pass": "Current password is incorrect."})
        if data['new_pass'] != data['re_enter_pass']:
               raise serializers.ValidationError({
                   "re_enter_pass": "Passwords do not match."
                   
                   }) 
        
        return data
        
        
                 
        
            
        