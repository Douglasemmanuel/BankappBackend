from django.shortcuts import render
from rest_framework.response import  Response
from .models import User , Account , AccountRequirement , Transaction , Reset , UserTransactionPin
from .serializers import UserSerializer , AccountSerializer , UserRegistrationSeraializer , AccountCreationSerializer , TransactionSerializer , UserTransactionSerializerPin
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from datetime import datetime , timedelta
from rest_framework import filters
from rest_framework import exceptions
from django.contrib.auth.hashers import make_password
from bank.renders import UserRenderer
import random
import string
from rest_framework.permissions import IsAdminUser , IsAuthenticated
# Create your  views here.


class UserRegistrationView(APIView):
    renderer_classes =  [UserRenderer]
    def post(self , request , format=None):
        serializer = UserRegistrationSeraializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
        



class UserAccountRegistrationView(APIView):

    def post(self, request , format=None):
        serializer = AccountCreationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    
class UserAccountView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request , format=None):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data ,status=status.HTTP_200_OK )


class MoneyTransactionView(APIView):
    def post(self, request , *args , **kwargs):
        sender_account_number = request.data.get('sender_account_number')
        receiver_account_number = request.data.get('receiver_account_number')
        amount = request.data.get('amount')

        try:
            sender_account = Account.objects.get(account_number=sender_account_number)
            receiver_account = Account.objects.get(account_number=receiver_account_number)
        except Account.DoesNotExist:
            return Response({"error":"Invalid account number"}, status=status.HTTP_400_BAD_REQUEST)
        
        if sender_account.balance < amount:
            return Response({"error":"Insuffient funds"}, status=status.HTTP_400_BAD_REQUEST)
        
        sender_account.balance -= amount
        receiver_account.balance += amount

        sender_account.save()
        receiver_account.save()

        seriailizer_sender = Account(sender_account)
        seriaizer_receiver = Account(receiver_account)

        response_data = {
            "sender_account": seriailizer_sender.data,
            "receiver_account": seriaizer_receiver.data,
        }
        print(response_data, amount + "have been  transfered to " + receiver_account_number)
        return Response(response_data , status=status.HTTP_200_OK)

class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request):
        user = request.user
        transcation = Transaction.objects.filter(user=user)
        serializer = TransactionSerializer(transcation , many=True)
        return Response(serializer.data)
    

class  ForgetApiView(APIView):
    def post(self,request):
        email = request.data['email']
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

        Reset.objects.create(
            email=email,
            token=token
        )

        url = 'http://localhost:3000/reset/' + token

        send_mail(
            subject='Reset your password!',
            message='Click <a href="%s">here</a> to reset your password!' % url,
            from_email='from@example.com',
            recipient_list=[email]
        )
        print(f" hey{email} your password reset Link {url}")
        return Response({
            'message': 'success',
        },status=status.HTTP_200_OK)



#to send a reset token to the user email
class ResetApiView(APIView):
    def post(self,request):
        data = request.data
        # password = request.password

        if data['password'] != data['password2']:
            raise exceptions.APIException('Passwords do not match!')

        reset_password = Reset.objects.filter(token=data['token']).first()

        if not reset_password:
            raise exceptions.APIException('Invalid link!')

        user = User.objects.filter(email=reset_password.email).first()

        if not user:
            raise exceptions.APIException('User not found!')

        user.set_password(data['password'])
        user.save()

        return Response({
            'message': 'Password successfully Changed'
        },status=status.HTTP_200_OK)
    



##user  transaction pin

class CreateTransactionPinView(APIView):
    def post(self, request, *args , **kwargs):
        user_profile =  UserTransactionPin.objects.get(user=request.user)
        if user_profile.transaction_pin:
            return Response({"details":"Treansaction Pin already exists."} , status=status.HTTP_400_BAD_REQUEST)
        
        pin = request.data.get('transaction_pin')
        if not pin or not pin.isdigit() or  len(pin) != 4:
            return Response({"detaiils":"Invalid PIN format."}, status=status.HTTP_400_BAD_REQUEST)

        user_profile.transaction_pin = pin
        user_profile.save()

        serializer = UserTransactionSerializerPin(user_profile)
        return Response(serializer.data , status=status.HTTP_201_CREATED)


class EditTransactionPinView(APIView):
    def put(self, request , *args , **kwargs):
        user_profile = UserTransactionPin.objects.get(user=request.user)
        pin = request.data.get('transaction_pin')
        if not pin or not pin.isdigit() or len(pin) != 4 :
            return Response({"detail":"Invalid PIN format"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_profile.transaction_pin = pin
        user_profile.save()

        serializer = UserTransactionSerializerPin(user_profile)
        return Response(serializer.data,status=status.HTTP_200_OK)


