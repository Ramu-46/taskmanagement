from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-task/', views.create_task, name='create_task'),
    path('employees/', views.employee_list, name='employee_list'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),  # you can define the view
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add-user/', views.add_user, name='add_user'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('notifications/', views.view_notifications, name='view_notifications'),
    path('', views.dashboard, name='dashboard'), 
    path('tasks/', views.all_tasks, name='all_tasks'), 
    path('all-tasks/', views.all_tasks, name='all_tasks'),
    path('employees/delete/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('employees/edit/<int:pk>/', views.add_or_edit_employee, name='edit_employee'),
    path('employees/add/', views.add_or_edit_employee, name='add_employee'),
]
