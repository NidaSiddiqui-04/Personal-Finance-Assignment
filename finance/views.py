from django.shortcuts import render,redirect,HttpResponse
from .form import Register
from django.contrib.auth import logout
from .form import TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transactions
from django.views.generic.edit import UpdateView,DeleteView
from django.db.models import Sum
import json
from django.db.models.functions import TruncMonth
from datetime import datetime 
import pandas as pd

# Create your views here.
def register(request):
    form=Register(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            
            user=form.save(commit=True)
            user.is_active=True
            user.save()
            user1=user.username
            messages.success(request,f"{user1}! You have been successfully registered. You can now log in")
            return redirect('finance:login')
    return render(request,'finance/register.html',{'form':form})    


def logout_view(request):
    logout(request)
    return render(request,'finance/logout.html')


@login_required
def form(request):
    form=TransactionForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            user=form.save(commit=False)
            user.user=request.user
            user.save()
            messages.success(request,"Transaction added successfully🎉")
            return redirect('finance:transaction_list')
    print(form.errors)    
    return render(request,'finance/transaction_form.html',{'form':form})    



def transaction_list(request):
    items=Transactions.objects.filter(user=request.user).order_by('-date')
    return render(request,'finance/transaction_list.html',{'items':items})

def update_transaction(request,id):
    form=TransactionForm(request.POST or None ,instance=Transactions.objects.get(id=id))
    if form.is_valid():
        form.save()
        return redirect('finance:transaction_list')
    context={
        'form':form,
    }
    return render(request,'finance/update.html',context)
    
def deleteform(request,id):
    form=Transactions.objects.get(id=id)
    form.delete()
    
    return redirect('finance:transaction_list')

@login_required(login_url='finance:login')
def dashboard(request):
    now=datetime.now()
    current_month=now.month
    current_year=now.year
    current_month_name=now.strftime('%B')
    
    transaction=Transactions.objects.filter(user=request.user).order_by('-date')

    income_agg = transaction.filter(type='Income',date__month=current_month,date__year=current_year).aggregate(total=Sum('amount'))
    total_income = income_agg['total'] or 0

    expense_agg = transaction.filter(type='Expense',date__month=current_month,date__year=current_year).aggregate(total=Sum('amount'))
    total_expense = expense_agg['total'] or 0

    balance=total_income-total_expense
    recent_transaction=transaction[:5]
    expense_by_category=(
        transaction.filter(type='Expense' ,date__month=current_month,date__year=current_year)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('category')
        
    )
    print(expense_by_category)
    
    categories=[item['category'] for item in expense_by_category]

    amount=[float(item['total']) for item in expense_by_category]
    print(categories)
    print(amount)
    monthly_expenses = (
    transaction.filter(type='Expense')
    .annotate(month=TruncMonth('date'))
    .values('month')
    .annotate(total=Sum('amount'))
    .order_by('month')
)

    months = [item['month'].strftime(" %B %Y") for item in monthly_expenses]
    monthly_totals = [float(item['total']) for item in monthly_expenses]
    

    context={
        'transaction':transaction,
        'total_income':total_income,
        'total_expense':total_expense,
        'balance':balance,
        'recent_transaction':recent_transaction,
        'categories':json.dumps(categories),
        'amount':json.dumps(amount),
        'months':json.dumps(months),
        'monthly_totals':json.dumps(monthly_totals),
        'current_month_name':current_month_name,
        "current_year":current_year
    }
    return render(request,'finance/dashboard.html',context)



@login_required(login_url='login')
def export_transactions_csv(request):
    transactions = Transactions.objects.filter(user=request.user).values(
        'date', 'type', 'category', 'amount', 'notes'
    )

    print(transactions)
    df = pd.DataFrame(list(transactions))

    
    messages.success(request,"your transaction have been successfully exported to csv file")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    
 
    df.to_csv(path_or_buf=response, index=False)
    
    return response