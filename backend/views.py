# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer,UserViewSerializer,UserProfileUpdateSerializer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
import jwt
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateAPIView








class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully",'status':True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!', 400)

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!', 400)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'id':user.id,
            'token': token,
            'message': 'Login successful',
            'status': True
        }
        return response
    

class UserView(APIView):
    def get(self, request, user_id):
        user = CustomUser.objects.filter(id=user_id).first()

        if not user:
            raise NotFound('User not found!')

        serializer = UserViewSerializer(user)
        return Response({
            'user_data': serializer.data,
            'message': 'User Profile View',
            'status': True
        })
    
class UserProfileEditView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Profile updated successfully',
            'status': True,
            'user_data': serializer.data
        })

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.filter(id=self.kwargs.get('pk')).first()
        if not obj:
            raise NotFound('User not found!')
        return obj
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout successful',
            'status': True
        }
        return response