from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Expenses, Category, Transaction, Savings
from .forms import UserRegistration, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime

@login_required
def home(request):

    date = datetime.now()

    data = {
        'categories': Category.objects.all(),
        'transactions': Transaction.objects.all(),
        'title': 'Expense Tracker',
        'date_now': date

    }
    return render(request, 'main/home.html', data)

@login_required
def analytics(request, date):

    date = datetime.now()

    path_ = request.path
    mo = path_[11:-5]
    if int(mo) < 10:
        month = '0' + mo
    else:
        month = mo
    year = path_[-5:-1]
    path_date = month + '-' + path_[-5:-1]

    print(month + year)
    print(str(date.month) + str(date.year))

    date1 = datetime(int(year), int(month), 1)
    date2 = datetime(int(date.year), int(date.month), 1)

    if date1 > date2:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    data = {
        'categories': Category.objects.all(),
        'transactions': Transaction.objects.all(),
        'title': 'Analytics',
        'date_now': date,
        'month': month,
        'year': year,
        'path_date': path_date,

    }
    return render(request, 'main/analytics.html', data)

def register(request):
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'User {username} has been created!')
            return redirect('login')
        else:
            messages.error(request, f'Nope')

    else:
        form = UserRegistration()
    return render(request, 'main/registration.html', {'form': form, 'title': 'Registration'})

@login_required
def profile(request):
    update_user = UserUpdateForm()

    data = {
        'update_user': update_user,
        'title': 'Profile'
    }

    return render(request, 'main/profile.html', data)

@login_required
def change_profile(request):
    if request.method == "POST":
        update_user = UserUpdateForm( request.POST, instance=request.user)
        if update_user.is_valid():
            update_user.save()
            messages.success(request, f'Account has been changed')
            return redirect('change_profile')
    else:
        update_user = UserUpdateForm(instance=request.user)

    data = {
        'update_user': update_user,
        'title': 'Update profile'
    }

    return render(request, 'main/change_profile.html', data)


class ShowTransations(LoginRequiredMixin, ListView):
    template_name = 'main/transactions.html'
    context_object_name = 'transactions'
    ordering = ['-date']
    paginate_by = 4

    def get_queryset(self):
        return Transaction.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwards):
        ctx = super(ShowTransations, self).get_context_data(**kwards)
        ctx['title'] = 'Transactions'
        return ctx

class AddCategory(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'color']
    template_name = 'main/add_category.html'

    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwards):
        ctx = super(AddCategory, self).get_context_data(**kwards)
        ctx['title'] = 'Add category'
        return ctx

class AddTransaction(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Transaction
    fields = ['expense', 'commentary']
    template_name = 'main/add_transaction.html'

    success_url = '/'

    #for s in request.path:
        #if s.isdigit():
            #category_id += s

    def form_valid(self, form):
        category_id = ''
        for s in self.request.path:
            if s.isdigit():
                category_id += s
        f_id = int(category_id)
        form.instance.category = Category.objects.get(pk=f_id)
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        category_id = ''
        for s in self.request.path:
            if s.isdigit():
                category_id += s
        f_id = int(category_id)
        category = Category.objects.get(pk=f_id)
        if self.request.user == category.owner:
            return True
        else:
            return False

    def get_context_data(self, **kwards):
        ctx = super(AddTransaction, self).get_context_data(**kwards)
        ctx['title'] = 'Add transaction'
        return ctx

class UpdateCategory(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name', 'color']
    template_name = 'main/update_category.html'

    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



    def test_func(self):
        expense = self.get_object()
        if self.request.user == expense.owner:
            return True
        else:
            return False

    def get_context_data(self, **kwards):
        ctx = super(UpdateCategory, self).get_context_data(**kwards)
        ctx['title'] = 'Update category'
        return ctx

class DeleteCategory(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'main/delete_category.html'

    success_url = '/'

    def test_func(self):
        expense = self.get_object()
        if self.request.user == expense.owner:
            return True
        else:
            return False

    def get_context_data(self, **kwards):
        ctx = super(DeleteCategory, self).get_context_data(**kwards)
        ctx['title'] = 'Delete category'
        return ctx


class ShowSavings(LoginRequiredMixin, ListView):
    model = Savings
    template_name = 'main/savings.html'
    context_object_name = 'savings'

    def get_context_data(self, **kwards):
        ctx = super(ShowSavings, self).get_context_data(**kwards)
        ctx['title'] = 'Savings'
        return ctx

class AddSaving(LoginRequiredMixin, CreateView):
    model = Savings
    fields = ['name', 'goal']
    template_name = 'main/add_saving.html'

    success_url = '/savings/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwards):
        ctx = super(AddSaving, self).get_context_data(**kwards)
        ctx['title'] = 'Add saving'
        return ctx

class UpdateSaving(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Savings
    fields = ['name', 'saved','goal']
    template_name = 'main/update_saving.html'

    success_url = '/savings/'

    #def get_absolute_url(self):
        #return reverse('savings')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        saving = self.get_object()
        if self.request.user == saving.owner:
            return True
        else:
            return False

    def get_context_data(self, **kwards):
        ctx = super(UpdateSaving, self).get_context_data(**kwards)
        ctx['title'] = 'Update saving'
        return ctx

class DeleteSaving(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Savings
    template_name = 'main/delete_saving.html'

    success_url = '/savings/'

    def test_func(self):
        saving = self.get_object()
        if self.request.user == saving.owner:
            return True
        else:
            return False

    def get_context_data(self, **kwards):
        ctx = super(DeleteSaving, self).get_context_data(**kwards)
        ctx['title'] = 'Delete saving'
        return ctx
