# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-task/', views.create_task, name='create_task'),
    path('employees/', views.employee_list, name='employee_list'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('add-employee/', views.add_employee, name='add_employee'),
]
