from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Reset)
admin.site.register(Transaction)
admin.site.register(AccountRequirement)
admin.site.register(UserTransactionPin)

