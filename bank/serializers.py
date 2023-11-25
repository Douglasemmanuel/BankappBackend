from rest_framework import serializers
from .models import Account , User , Transaction  , AccountRequirement , UserTransactionPin
from rest_framework_simplejwt.tokens import RefreshToken
# import uuid
from .utils import  generate_account_number ,  generate_bvn_number

class UserRegistrationSeraializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        models = User
        fields = '__all__'
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password and confirm password doesnt match")
        return attrs
    def create(self , validate_data):
        return User.objects.create_user(**validate_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AccountCreationSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class  Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('account_number',)

    def create(self, validated_data):
        validated_data['account_number'] = generate_account_number()
        return super(AccountCreationSerializer, self).create(validated_data)()


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'



class BvnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountRequirement
        fields = '__all__'

class BvnCreationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        read_only_fields = ('bvn',)

    def create(self, validated_data):
        validated_data['bvn'] = generate_bvn_number()
        return super(BvnCreationSerializer, self).create(validated_data)()
    

# class TransactionCreationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class UserTransactionSerializerPin(serializers.ModelSerializer):
    class Meta:
        model = UserTransactionPin
        fields = '__all__'


