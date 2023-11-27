from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser
import uuid
from django.dispatch import receiver
from django.db.models.signals import pre_save
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email ,first_name,last_name, phonenumber , password=None , password2=None):
        if not email:
            raise ValueError('Users must have an email address')  
      
        user = self.model(
            email = self.normalize_email(email),
            # name=name,
            first_name=first_name,
            last_name=last_name,
            phonenumber=phonenumber
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,first_name,last_name,phonenumber , password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,

            phonenumber=phonenumber
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email= models.EmailField(max_length=225 , unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    phonenumber = models.CharField(max_length=15,unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name' , 'phonenumber']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Account(models.Model):
    ACCOUNT_TYPES = [
        ('savings' , 'savings Account'),
        ('current' , 'current Account'),
        # ('naira' , 'naira Account'),
        # ('euro' , 'euro Account'),
        # ('usdollar' , 'usdollar Account'),
        # ('candollar' , 'candollar Account'),
        

    ]
    user = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    account_name = models.CharField(max_length=225 )
    createdAt = models.DateTimeField(auto_now_add=True)
    account_number = models.CharField(max_length=11 , unique=True)
    account_verified = models.BooleanField(default=False)
    account_type = models.CharField(max_length=10 , choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=30 ,decimal_places=2 )
    # sort_code = models.CharField(max_length=6 , unique=True)
    # iban = models.CharField(max_length=22 , unique=True)

    def __str__(self):
        return str(self.account_name)
    
    # def save(self, *args , **kwargs):
    #     if not self.account_number:
    #         self.account_number = '' .join(str(uuid.uuid4().int)[:10])

    #     if not self.sort_code:
    #         self.sort_code = '' .join(str(uuid.uuid4().int)[:6])
        
    #     if not self.iban:
    #         self.iban = '' .join(str(uuid.uuid4().int)[:20])

    # @receiver(pre_save , sender=Account)
    def generate_account_details(sender, instance , **kwargs):
        if not instance.account_number:
            instance.account_number = '' .join(str(uuid.uuid4().int)[:10])

        # if not instance.sort_code:
        #     instance.sort_code = '' .join(str(uuid.uuid4().int)[:6])
        
        # if not instance.iban:
        #     instance.iban = 'ED' + '' .join(str(uuid.uuid4().int)[:20])


   
class AccountRequirement(models.Model):
    user = models.ForeignKey(Account , on_delete=models.SET_NULL , null=True),
    bvn = models.CharField(max_length=12 , unique=True)
    createdAt = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    sender = models.ForeignKey(Account ,related_name='sender', on_delete=models.CASCADE )
    receiver = models.ForeignKey(Account ,related_name='receiver', on_delete=models.CASCADE )
    createdAt = models.DateTimeField(auto_now_add=True)
    amount=models.DecimalField(max_digits=20 , decimal_places=2)

    def __str__(self):
        return self.sender + ':' + self.receiver


class Reset (models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)


class UserTransactionPin(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    transaction_pin = models.CharField(max_length=4 , null=True , blank=True)


