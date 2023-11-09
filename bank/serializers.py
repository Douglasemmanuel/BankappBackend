from rest_framework import serializers
from .models import Account , User , Transaction 
import uuid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class  Meta:
        model = Account
        fields = '__all__'