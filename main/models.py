from django.db import models
from django.contrib.auth.models import User
from colorful.fields import RGBColorField
from django.urls import reverse
from django.utils import timezone
import random
import uuid


r = lambda: random.randint(0,255)

class Expenses(models.Model):
    category_name = models.CharField(max_length = 30)
    expense = models.DecimalField(default=0, decimal_places=2, max_digits=15)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    color = RGBColorField(verbose_name= (u'Color'), max_length=7, \
        default='#%02X%02X%02X' % (r(),r(),r()))

    def get_absolute_url(self):
        return reverse('home')

class Category(models.Model):
    name = models.CharField(max_length=30)
    color = RGBColorField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    category = models.ForeignKey(main_category, on_delete=models.CASCADE)
    expense = models.DecimalField(decimal_places=2, max_digits=15)
    commentary = models.TextField(max_length=200, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

class Savings(models.Model):
    name = models.CharField(max_length = 30)
    goal = models.DecimalField(decimal_places = 2, max_digits = 15)
    saved = models.DecimalField(default = 0, decimal_places = 2, max_digits = 15)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
