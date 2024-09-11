from django.db import models
from django.core.validators import RegexValidator
import uuid
import random

# Create your models here.


class Bank_branches(models.Model):
    def __str__(self):
        return f"{self.branch_name}-{self.branch_id}"
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)



class AccountNumber(models.Model):
    account_number = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(r'^\d{12}$', 'Account number must be exactly 12 digits.')
        ],
        unique=True
    )

    def __str__(self):
        return self.account_number

class Account(models.Model):
    account_choices = [
        ('current', 'Current'),
        ('savings', 'Savings')
    ]
    account_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    account_type = models.CharField(max_length=10, choices=account_choices)
    balance = models.FloatField(default=0)
    account_number = models.ForeignKey(AccountNumber, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('account_number', 'account_type'),)

    def __str__(self):
        return f"{self.account_type} - {self.account_id}"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60,null=False)
    phone_no = models.CharField(max_length=10,
                                    unique=True,
                                    validators=[
                                        RegexValidator(r'^\d{10}$')
                                    ],null=False)
    Aadhar_no = models.CharField(max_length=12,
                                    unique=True,
                                    validators=[
                                        RegexValidator(r'^\d{12}$')
                                    ],null=False)
    DOB = models.DateField()
    branch_connect = models.ForeignKey(Bank_branches,on_delete=models.CASCADE)
    account = models.OneToOneField(AccountNumber,on_delete = models.CASCADE)
    password = models.CharField(max_length = 128,null=False,blank=False,
                                validators=[
                                    RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)')
                                ])
    def __str__(self):
        return f"{self.name} - {self.account}"

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100,primary_key=True,editable=False)
    transaction_details = models.TextField(max_length=120)
    transaction_type = models.CharField(max_length=70)
    transaction_date = models.DateField()
    transaction_from = models.ForeignKey(AccountNumber,related_name='transactions_from',on_delete=models.CASCADE)
    transaction_to = models.ForeignKey(AccountNumber,related_name='transactions_to',null=True,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super(Transaction, self).save(*args, **kwargs)

    def generate_transaction_id(self):
        # Generate a unique ID using UUID
        return str(uuid.uuid4())
    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_from}"

    
    




# Create your models here.
