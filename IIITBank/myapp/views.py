from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q
from .models import Bank_branches,AccountNumber,Transaction,Customer,Account
import random
from datetime import datetime,date

# Create your views here.
generated_numbers = set()

def gen_12_digit_number():
    random_number = random.randint(100000000000,999999999999)
    if  random_number not in generated_numbers:
        generated_numbers.add(random_number)
        return random_number
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def starting_page(request):
    return render(request,'myapp/startingPage.html')



# Create your views here.
def CreatePage(request):
    branches = Bank_branches.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        #to check if phone number present in database or not
        if phone_no:
            all_customers = Customer.objects.all()
            for i in all_customers:
                print(i)
                if i.phone_no == phone_no:
                    print("true")
                    error = "phone_num"
                    return render(request,'myapp/error.html',{'error':error})
                
        aadhar_no = request.POST.get('Aadhar_no')
        #to check if aadhar number present in database or not
        if aadhar_no:
            all_customers = Customer.objects.all()
            for i in all_customers:
                if i.Aadhar_no == aadhar_no:
                    error = "aadhar_num"
                    return render(request,'myapp/error.html',{'error':error})
                
        DOB = request.POST.get('DOB')
        #to check age about 18
        if DOB:
            dob = datetime.strptime(DOB, '%Y-%m-%d').date()
            age = calculate_age(dob)
            if age < 18:
                error_message = 'You must be at least 18 years old to open a account.'
                return render(request, 'myapp/error.html', {'error_message': error_message})
        branch_id = request.POST.get('branch')
        password = request.POST.get('password')
        Account_number = gen_12_digit_number()
        
        branch = Bank_branches.objects.get(branch_id=branch_id)
        accountNumber = AccountNumber(account_number = Account_number)
        customer = Customer(name=name,phone_no=phone_no,Aadhar_no=aadhar_no,DOB=DOB,branch_connect = branch,password=password,account=accountNumber)
        account = Account(account_type = 'current',account_number=accountNumber)
        accountNumber.save()
        customer.save()
        account.save()
        return redirect(f'/accountNumber/{Account_number}')
    return  render(request,'myapp/CreatePage.html',{'branches':branches,})

#showing account number page
def showAccountNum(request, account_num):
    account = AccountNumber.objects.get(account_number=account_num)
    customer = Customer.objects.get(account = account)
    return render(request,'myapp/accountNum.html',{'customer':customer})

def mainPage(request,customer_id):
    customer = Customer.objects.get(customer_id=customer_id)
    return render(request,'myapp/main.html',{'customer':customer})

def loginPage(request):
    allcustomer = Customer.objects.all()
    context = {}
    if request.method=='POST':
        username = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        aadhar_no = request.POST.get('Aadhar_no')
        password = request.POST.get('password')
        for customer in allcustomer:
            if customer.name == username and customer.phone_no == phone_no and customer.Aadhar_no ==aadhar_no and customer.password == password:
                return redirect(f'/main/{customer.customer_id}')
        context['invalid_credentials'] = True 
                
        
    return render(request,'myapp/loginpage.html',context)

def checkBalance(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account = account)
    account_details = Account.objects.get(account_number=account)
    return render(request,'myapp/checkbalance.html',{'customer':customer,'account_details':account_details})

def deposit(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account = account)
    account_details = Account.objects.get(account_number=account)
    if request.method == 'POST':
        amount = request.POST.get('deposit')
        account_details.balance += float(amount)
        account_details.save()
        transaction = Transaction(transaction_details = "successfully deposited rs"+amount,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=None)
        transaction.save()
        return redirect(f'/main/{customer.customer_id}?success=true')
    return render(request,'myapp/deposit.html',{'customer':customer,'account_details':account_details})

def upi(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account = account)
    account_details = Account.objects.get(account_number=account)
    customers = Customer.objects.all()
    context1 = {'transaction':None}
    if request.method == 'POST':
        account_num = request.POST.get('account_no')
        amount = request.POST.get('transact')
        
        if account_num == account_no:
            transaction = Transaction(transaction_details = "invalid transaction",transaction_type='failed',transaction_date=date.today(),transaction_from=account,transaction_to=account)
            transaction.save()
            return render(request,'myapp/upi.html',{'customer':customer,'account_details':account_details,'transaction':'same'})
        for i in customers:
            if i.account.account_number == account_num:
                account_to = AccountNumber.objects.get(account_number=account_num)
                if account_details.balance - float(amount)<0:
                    transaction = Transaction(transaction_details = "insufficient funds tried to transact amount:"+ amount,transaction_type='failed',transaction_date=date.today(),transaction_from=account,transaction_to=account_to)
                    transaction.save()
                    return render(request,'myapp/upi.html',{'customer':customer,'account_details':account_details,'transaction':'failed'})
                
                account_details_to = Account.objects.get(account_number = account_to)
                customer_to = Customer.objects.get(account = account_to)
                account_details.balance -= float(amount)
                account_details_to.balance += float(amount)
                account_details.save()
                account_details_to.save()
                transaction = Transaction(transaction_details = "successfully transfered amount:"+ amount,transaction_type='success',transaction_date=date.today(),transaction_from=account,transaction_to=account_to)
                transaction.save()
                return render(request,'myapp/upi.html',{'customer':customer,'account_details':account_details,'customer_to':customer_to,'account_details_to':account_details_to,'transaction':'pass'})
        transaction = Transaction(transaction_details = "transferring amount to invalid account",transaction_type='failed',transaction_date=date.today(),transaction_from=account,transaction_to=None)
        transaction.save()
        return render(request,'myapp/upi.html',{'customer':customer,'account_details':account_details,'transaction':'noAccountAvail'})
    return render(request,'myapp/upi.html',{'customer':customer,'account_details':account_details})

    
def transaction(request,account_no):
    account = AccountNumber.objects.get(account_number=account_no)
    customer = Customer.objects.get(account=account)
    account_details = Account.objects.get(account_number=account)
    combined_transactions = Transaction.objects.filter(
    Q(transaction_from=account) | Q(transaction_to=account))
    
    return render(request,'myapp/transaction.html',{'com_trans':combined_transactions,'customer':customer})

