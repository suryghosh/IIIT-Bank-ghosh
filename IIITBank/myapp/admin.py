from django.contrib import admin
from .models import Customer,Bank_branches,AccountNumber,Account,Transaction
# Register your models here.
admin.site.register(Bank_branches)
admin.site.register(Customer)
admin.site.register(AccountNumber)
admin.site.register(Account)
admin.site.register(Transaction)
