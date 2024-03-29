# views.py
import datetime

import jwt
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, ShippingRegistration, Contactus
from .serializers import (UserSerializer, UserViewSerializer, UserProfileUpdateSerializer, ContactusSerializer,
                          ShippingRegSerializer, ShippingRegUpdateSerializer)


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully", 'status': True}, status=status.HTTP_201_CREATED)
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
            'id': user.id,
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


class UserDeleteView(APIView):
    def delete(self, request, pk):
        try:
            instance = CustomUser.objects.get(pk=pk)
            instance.delete()
            return Response({"message": "User deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout successful',
            'status': True
        }
        return response


class ContactUsView(APIView):
    def post(self, request):
        serializer = ContactusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'success',
            'status': True,
            'user_data': serializer.data
        }
        )


class ContactUsGetView(APIView):
    def get(self, request):
        contact = Contactus.objects.all()
        Contact = ContactusSerializer(contact, many=True)
        return Response(Contact.data)

class ContactUsDeleteView(APIView):
    def delete(self, request, pk):
        try:
            instance = Contactus.objects.get(pk=pk)
            instance.delete()
            return Response({"message": "Message deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)
        except Contactus.DoesNotExist:
            return Response({"message": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ShippingRegView(APIView):
    def post(self, request):
        serializer = ShippingRegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Shipping registered successfully.',
                'status': True,
                'consignment_data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShippingReggetView(ListAPIView):
    serializer_class = ShippingRegSerializer

    def get_queryset(self):
        user = self.kwargs['user_id']
        return ShippingRegistration.objects.filter(user_id=user)


class ShippingRegEditView(RetrieveUpdateAPIView):
    queryset = ShippingRegistration.objects.all()
    serializer_class = ShippingRegUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Shipping Registration Data Updated Successfully',
            'status': True,
            'user_data': serializer.data
        })

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.filter(id=self.kwargs.get('pk')).first()
        if not obj:
            raise NotFound('User not found!')
        return obj


class ShippingRegistrationDeleteView(APIView):
    def delete(self, request, pk):
        try:
            instance = ShippingRegistration.objects.get(pk=pk)
            instance.delete()
            return Response({"message": "Shipping registration deleted successfully."},
                            status=status.HTTP_204_NO_CONTENT)
        except ShippingRegistration.DoesNotExist:
            return Response({"message": "Shipping registration not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
