# Generated by Django 4.2.4 on 2023-10-12 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(choices=[('Employee', 'Employee'), ('Business', 'Business'), ('Student', 'Student'), ('Other', 'Other')], max_length=10)),
                ('Savings_Percentage', models.DecimalField(decimal_places=3, max_digits=5)),
                ('Savings', models.DecimalField(decimal_places=2, max_digits=10)),
                ('income', models.BigIntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(choices=[('Expense', 'Expense'), ('Income', 'Income')], max_length=10)),
                ('Expense_amount', models.BigIntegerField()),
                ('Date', models.DateField(default=django.utils.timezone.now)),
                ('Category', models.CharField(choices=[('Food', 'Food'), ('Travel', 'Travel'), ('Shopping', 'Shopping'), ('Necessities', 'Necessities'), ('Entertainment', 'Entertainment'), ('Other', 'Other')], default='Food', max_length=20)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]