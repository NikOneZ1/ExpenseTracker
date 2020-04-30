from django.urls import path
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.register, name = 'register'),
    path('login/', authViews.LoginView.as_view(template_name='main/login.html'), name = 'login'),
    path('logout/', authViews.LogoutView.as_view(template_name='main/logout.html'), name = 'logout'),
    path('profile/', views.profile, name = 'profile'),
    path('profile/change_profile/', views.change_profile, name = 'change_profile'),
    path('add_category/', views.AddCategory.as_view(), name = 'add_category'),
    path('update_category-<int:pk>/', views.UpdateCategory.as_view(), name = 'update_category'),
    path('delete_category-<int:pk>/', views.DeleteCategory.as_view(), name = 'delete_category'),
    path('add_transaction-<int:pk>/', views.AddTransaction.as_view(), name = 'add_transaction'),
    path('transactions/', views.ShowTransations.as_view(), name = 'transactions'),
    path('analytics-<int:date>/', views.analytics, name = 'analytics'),
    path('savings/', views.ShowSavings.as_view(), name = 'savings'),
    path('add_saving/', views.AddSaving.as_view(), name = 'add_saving'),
    path('update_saving-<int:pk>/', views.UpdateSaving.as_view(), name='update_saving'),
    path('delete_saving-<int:pk>/', views.DeleteSaving.as_view(), name = 'delete_saving'),
]
