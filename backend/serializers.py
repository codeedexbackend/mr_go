from django.utils.text import slugify
from rest_framework import serializers

from .models import CustomUser, Contactus, ShippingRegistration


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    mobile = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'password', 'password2', 'mobile']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError({"Error": "Passwords do not match"})
        return data

    def validate_mobile(self, value):
        if CustomUser.objects.filter(mobile=value).exists():
            raise serializers.ValidationError("Mobile number already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)

        email = validated_data.get('email')

        username = slugify(email.split('@')[0])
        count = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{slugify(email.split('@')[0])}_{count}"
            count += 1

        instance = self.Meta.model(**validated_data, username=username)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ContactusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactus
        fields = '__all__'


class ShippingRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRegistration
        fields = '__all__'


class ShippingRegUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRegistration
        fields = '__all__'
