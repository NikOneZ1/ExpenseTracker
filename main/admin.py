from django.contrib import admin
from .models import Expenses, Category, Transaction, Savings

admin.site.register(main_expenses)
admin.site.register(main_category)
admin.site.register(main_transaction)
admin.site.register(main_savings)
