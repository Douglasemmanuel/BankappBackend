from django.urls import path
# from backend.views  import 
from .views import UserRegistrationView , UserAccountRegistrationView , UserAccountView , CreateTransactionPinView ,EditTransactionPinView , ResetApiView , ForgetApiView 
urlpatterns = [
    #User Api end-point
    path('user/register/',UserRegistrationView.as_view(), name='registration'),


    #Account Api end-point
    path('account/create/' , UserAccountRegistrationView.as_view() , name='account-creation'),
    path('acount/' , UserAccountView.as_view(), name='account'),
    path('transactionpin/create/' , CreateTransactionPinView.as_view() ,name='transactionpin-create' ),
    path('transactionpin/edit' , EditTransactionPinView.as_view() , name='transactionpin-edit'),
]