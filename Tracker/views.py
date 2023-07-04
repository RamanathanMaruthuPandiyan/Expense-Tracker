import datetime
import calendar
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.contrib.sessions.backends.db import SessionStore
from django.db.models.functions import *
from django.db.models import Sum
from .models import *
import pandas as pd
# Create your views here.
# --------------------------------------------------------------------------
# Index Page.
def Home(request):
    return render(request,'Home/index.html')
# --------------------------------------------------------------------------
# Dashboard
# --------------------------------------------------------------------------
@login_required
def Admin(request):
    wtsum=0
    isum=0
    user_id = request.session["user_id"]
    user=User.objects.get(id=user_id)
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    expenses=Expenses.objects.filter(user=user).order_by('-Date')
    Weekly=Expenses.objects.filter(user=user,Type="Expense",Date__gte=one_week_ago,Date__lte=todays_date).values('Category').annotate(Total_Expenses=Sum('Expense_amount')).order_by('Category')
    Monthly=Expenses.objects.filter(user=user,Type="Expense").annotate(month=ExtractMonth('Date')).values('month').annotate(Total_Expenses=Sum('Expense_amount')).order_by()
    IMonthly=Expenses.objects.filter(user=user,Type="Income").annotate(month=ExtractMonth('Date')).values('month').annotate(Total_Income=Sum('Expense_amount')).order_by()
    Yearly=Expenses.objects.filter(user=user,Type="Expense").annotate(year=ExtractYear('Date')).values('year').annotate(Total_Expenses=Sum('Expense_amount')).order_by()
    if len(IMonthly)!=0:
        df=pd.DataFrame(IMonthly)
        df9=df.Total_Income.tolist()
        isum=sum(df9)
    if len(Weekly)!=0:
        df=pd.DataFrame(Weekly)
        df1=df.Category.tolist()
        df2=df.Total_Expenses.tolist()
        i=0
        wtsum=sum(df2)

    if len(Monthly)!=0:
        df=pd.DataFrame(Monthly)
        df5=[]
        df3=df.month.tolist()
        for x in df3:
            df5.append(calendar.month_abbr[x])
        df4=df.Total_Expenses.tolist()
    if len(Yearly)!=0:
        df=pd.DataFrame(Yearly)
        df6=df.year.tolist()
        df7=df.Total_Expenses.tolist()
    sum1=0
    sum2=0
    i=0
    for i in expenses:
        if i.Type=='Expense':
            sum1+=i.Expense_amount
        else:
            sum2+=i.Expense_amount
    x= user.userprofile.Savings+sum2 - sum1
    y=0
    if x<0:
        messages.warning(request,'Your expenses exceeded your savings')
        y=x
    i=0

    wsave=user.userprofile.income-wtsum
    return render(request,'Home/Dashboard.html',locals())

@login_required
def Logout(request):
    del request.session['user_id']
    logout(request)
    return redirect('home')

@login_required
def AddExp(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    if request.method == "POST":
        choice = request.POST.get("choices")
        amount= request.POST.get("amount")
        Date = request.POST.get("date")
        Category = request.POST.get("category")
        Add_Exp = Expenses(user = user1,Type=choice,Expense_amount=amount,Date = Date,Category= Category)
        Add_Exp.save()
        return redirect('add-expenses')
    else:
        expenses_user1=Expenses.objects.filter(user=user1).order_by('-Date')
        paginator = Paginator(expenses_user1, 10)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {
            'page_obj' : page_obj,
        }
        return render(request,'Home/Add-Expenses.html',locals())

@login_required
def expense_delete(request,id):
        expenses = Expenses.objects.get(id=id)
        expenses.delete()
        return redirect('add-expenses')

@login_required
def expense_edit(request,id):
        expenses = Expenses.objects.get(id=id)
        return render(request,'Home/expense_edit.html',locals())

@login_required
def Expense_update(request,id):
    if request.method == "POST":
        add = Expenses.objects.get(id=id)
        add.add_money = request.POST["choices"]
        add.quantity = request.POST["amount"]
        add.Date = request.POST["date"]
        add.Category = request.POST["category"]
        add .save()
        return redirect('add-expenses')
    else:
        return redirect('add-expenses')

@login_required
def profile(request):
    return render(request,'Home/User-Profiles.html')

@login_required
def profile_edit(request,id):
    add = User.objects.get(id=id)
    return render(request,'Home/User-Profiles-Edit.html',{'add':add})


# -----------------------------------------------------------------------------------------
# Profile_Update
def profile_update(request,id):
    if request.method == "POST":
        user = User.objects.get(id=id)
        user.first_name = request.POST["fname"]
        user.last_name = request.POST["lname"]
        user.email = request.POST["email"]
        income=request.POST.get('income')
        Save_Per=float(request.POST['savings_per'])/100
        Savings=(Save_Per)*int(income)
        user.userprofile.income = income
        user.userprofile.Savings = Savings
        user.userprofile.Savings_Percentage = Save_Per
        user.userprofile.profession = request.POST["profession"]
        user.userprofile.save()
        user.save()
        return redirect("user-profile")


# -----------------------------------------------------------------------------------------
# Login and Register.
"""This for Login"""
def Login(request):
    if request.method=="POST":
        login_user=request.POST.get('log_user')
        login_pass=request.POST.get('log_pass')
        user = authenticate(username = login_user, password = login_pass)
        if user is not None:
            auth.login(request,user)
            request.session['is_logged'] = True
            user = request.user.id
            request.session["user_id"] = user
            messages.success(request, " Successfully logged in")
            return redirect('dashboard')
        else:
            return render(request,'Authentication/Login.html',{'err':'Invalid Credentials'})
    else:
        return render(request,'Authentication/Login.html')


"""This for Registration"""
def Register(request):
    if request.method=="POST":
        Reg_User = request.POST['User_Name']
        Reg_first_name=request.POST['fname']
        Reg_last_name=request.POST['lname']
        profession=request.POST.get('profession')
        income=request.POST.get('income')
        Save_Per=float(request.POST.get('savings_per'))/100
        Savings=(Save_Per)*int(income)
        Reg_Email = request.POST.get('email')
        Reg_Pass = request.POST.get('password')
        Re_Reg_Pass=request.POST.get('confirm_password')  
        profile = UserProfile(Savings = Savings,Savings_Percentage=Save_Per,profession=profession,income=income)
        if request.method=='POST':
            try:
                user_exists=User.objects.get(username=Reg_User)
                if user_exists is not None:
                    return render(request,'Authentication/Register.html',{'err':'Username Already Exist!!'})
            except:
                if len(Reg_User)>8:
                    return render(request,'Authentication/Register.html',{'err':' Username must be max 8 characters, Please try again'})
                if not Reg_User.isalnum():
                    return render(request,'Authentication/Register.html',{'err':'Username should only contain letters and numbers, Please try again'})
                if Reg_Pass!=Re_Reg_Pass:
                    return render(request,'Authentication/Register.html',{'err':'Password did not Match'})
        user = User.objects.create_user(Reg_User, Reg_Email, Reg_Pass)
        user.first_name=Reg_first_name
        user.last_name=Reg_last_name
        user.email=Reg_Email
        user.save()
        profile.user = user
        profile.save()
        return redirect('login')
    else:
        return render(request,'Authentication/Register.html')



#-------------------------------------------------------------------------------------------------------------------------------------
#Logic For Computation----------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------
