# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from .models import User
class UserRegistraion(APIView):

    permission_classes = [AllowAny]
    def post(self, request):

        user_data ={
            'username':request.data.get("username"),
            'first_name':request.data.get("firstname"),
            'last_name':request.data.get("lastname"),
            'email':request.data.get("email"),
            'is_moderator':request.data.get("is_moderator"),
            'password':request.data.get("password"),
            'password2':request.data.get("password2"),
        }

        serializer = UserRegistrationSerializer(data = user_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):

    permission_classes = [AllowAny]

    def post(self,request):

        user_data = {
            'email': request.data.get("email"),
            'password': request.data.get("password"),
        }

        serializer = UserLoginSerializer(data=user_data);
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)