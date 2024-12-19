from rest_framework import serializers
from .models import *

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signup
        fields = ['id', 'Name', 'Password']
        extra_kwargs = {'Password': {'write_only': True}}

class ApiDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiData
        fields = '__all__'
