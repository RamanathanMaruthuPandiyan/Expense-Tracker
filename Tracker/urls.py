from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('login',views.Login, name='login'),
    path('logout',views.Logout, name='logout'),
    path('userregister',views.Register,name='userregister'),
    path('dashboard',views.Admin, name='dashboard'),
    path('add-expenses',views.AddExp, name='add-expenses'),
    path('user-profile',views.profile, name='user-profile'),
    path('<int:id>/profile_edit',views.profile_edit,name='profile_edit'),
    path('<int:id>/profile_update',views.profile_update,name='profile_update'),
    path('expense_edit/<int:id>',views.expense_edit,name='expense_edit'),
    path('<int:id>/expense_delete',views.expense_delete,name='expense_delete'),
    path('expense_update/<int:id>', views.Expense_update, name="expense_update"),

]
