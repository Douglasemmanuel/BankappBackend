from django.urls import path
# from backend.views  import 
from .views import UserRegistrationView , UserAccountRegistrationView , UserAccountView , CreateTransactionPinView ,EditTransactionPinView , ResetApiView , ForgetApiView ,GetAllUsers, GetUserByIdView , UserLoginView 
    
urlpatterns = [
    #User Api end-point
    path('user/register/',UserRegistrationView.as_view(), name='registration'),
    path('user/login/' , UserLoginView.as_view(), name='login'),

    #Account Api end-point
    path('account/create/' , UserAccountRegistrationView.as_view() , name='account-creation'),
    path('acount/' , UserAccountView.as_view(), name='account'),
    path('transactionpin/create/' , CreateTransactionPinView.as_view() ,name='transactionpin-create' ),
    path('transactionpin/edit' , EditTransactionPinView.as_view() , name='transactionpin-edit'),



    #Admin Endpoint

    path('user/' , GetAllUsers.as_view(), name='all-users'),
    path('user/<str:pk>/',GetUserByIdView.as_view(),name='getuserbyid'),
    # path('user/'),
]