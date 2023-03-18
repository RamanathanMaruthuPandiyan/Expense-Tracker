from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.

SELECT_CATEGORY_CHOICES = [
    ("Food","Food"),
    ("Travel","Travel"),
    ("Shopping","Shopping"),
    ("Necessities","Necessities"),
    ("Entertainment","Entertainment"),
    ("Other","Other")
]
ADD_EXPENSE_CHOICES = [
     ("Expense","Expense"),
     ("Income","Income")
 ]
PROFESSION_CHOICES =[
    ("Employee","Employee"),
    ("Business","Business"),
    ("Student","Student"),
    ("Other","Other")
]
class Expenses(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    Type = models.CharField(max_length = 10 , choices = ADD_EXPENSE_CHOICES )
    Expense_amount = models.BigIntegerField()
    Date = models.DateField(default = now)
    Category = models.CharField( max_length = 20, choices = SELECT_CATEGORY_CHOICES , default ='Food')

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profession = models.CharField(max_length = 10, choices=PROFESSION_CHOICES)
    Savings_Percentage=models.DecimalField(max_digits = 5,decimal_places = 3)
    Savings = models.DecimalField(max_digits = 10,decimal_places = 2)
    income = models.BigIntegerField(null=True, blank=True)
    def __str__(self):
       return self.user.username
