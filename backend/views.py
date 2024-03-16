# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, LoginSerializer,UserViewSerializer
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
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid email or password.', 400)

        token = RefreshToken.for_user(user)
        token_lifetime = datetime.timedelta(minutes=60)  # Token expiration time
        token['exp'] = datetime.datetime.utcnow() + token_lifetime

        response_data = {
            'id': user.id,
            'token': str(token.access_token),
            'token_expiry': token['exp'],
            'message': 'Login successful',
            'status': True
        }

        return Response(response_data)
    

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
    serializer_class = UserSerializer

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
        # Only allow users to update their own profile
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