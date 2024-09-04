from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .models import Profile
from contacts import models, serializers, views
from .serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import authenticate




class ListProfile(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)
    

class ListUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]



class Register(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        email = '' if request.data.get('email') == None else request.data.get('email')
        
        if not name or not phone_number:
            return Response(
                {"Error": "Both name and phone_number are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {"Error": "Password is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            exist_user = User.objects.get(username=phone_number)
            serializer = UserSerializer(exist_user)
            if serializer.data['username']:
                return Response(
                    {"Error": "User already registered with this phone number"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            try:
                with transaction.atomic():
                    user = User(
                    first_name=name,
                    username=phone_number,
                    email=email
                    )
                    user.set_password(password)
                    user.save()

                    profile = Profile.objects.create(
                        user = user,
                        name = name,
                        phone_number = phone_number,
                        email = email
                    )
                    
                    profile_serializer = ProfileSerializer(profile)

                    contact = models.Contact.objects.create(
                        name = name,
                        phone_number = phone_number,
                        email = email,
                        user_id = profile_serializer.data['id']
                    )

                    return Response(
                        {"Message": "Registered successfully"},
                        status=status.HTTP_200_OK
                    )
            except Exception as e:
                return Response(
                    {"Message": f"Error during Signup: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            

class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if username is None or password is None:
            return Response({"Error": "Username and Password both required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"Token": token.key}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"Message": f"Error during SignIn: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({"Error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)