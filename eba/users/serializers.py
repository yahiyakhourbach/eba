from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import re

class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=60,min_length=8,write_only=True);
    password2 = serializers.CharField(max_length=60,min_length=8,write_only=True);
    
    class  Meta:
        model = User
        fields = ["first_name","last_name","username","email","is_moderator","password","password2"]
    
    def validate(self,attrs):

        errors          = {}
        valid_string    = re.compile(r'^[A-Za-z]+$')
        contain_letter  = re.compile(r'[A-Za-z]')
        white_space     = re.compile(r'\s')
        special_chars   = re.compile(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]+')
        numbers         = re.compile(r'\d')
        
        if attrs["password"] != attrs["password2"] :
            errors["password"] = "password mismatch"
        
        if len(attrs.get("username")) < 5 or white_space.search(attrs.get("username")):
            errors["username"] = "username too short or it contain spaces"

        if  not valid_string.match(attrs["first_name"]):
             errors["first_name"] = "firstname should contain only letters"

        if  not valid_string.match(attrs["last_name"]):
             errors["last_name"] = "firstname should contain only letters"

        if not numbers.search(attrs["password"]) or \
            not contain_letter.search(attrs["password"]) or \
            not special_chars.search(attrs["password"]):
                errors["password"] = "password should contain at \
                    least 8 characters one digit and one special \
                    character and a letter"

        if errors:
             raise serializers.ValidationError(errors)
        return attrs
    
    def create(self, validated_data):

        validated_data.pop("password2",None)
        user = User.objects.create_user(
            first_name      = validated_data["first_name"],
            last_name       = validated_data["last_name"],
            username        = validated_data["username"],
            email           = validated_data["email"],
            password        = validated_data["password"],
            is_moderator    = validated_data["is_moderator"]
        )
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):

    email           = serializers.EmailField(max_length=150,write_only = True)
    password        = serializers.CharField(max_length=255,write_only = True)
    access          = serializers.CharField(max_length=255,read_only = True)
    refresh         = serializers.CharField(max_length=255,read_only = True)
    is_moderator    = serializers.BooleanField(default=False)
    class Meta:
        model = User
        fields = ["email","is_moderator","access","refresh","password"]

    def validate(self,attrs):
        email       = attrs.get("email")
        password    = attrs.get("password")

        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Email doesn't exist.")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials")
        
        refresh  = RefreshToken.for_user(user)
        return {
                "is_moderator":user.is_moderator,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
