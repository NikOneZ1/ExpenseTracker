from django.contrib import admin
from .models import Expenses, Category, Transaction, Savings

admin.site.register(Expenses)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Savings)
