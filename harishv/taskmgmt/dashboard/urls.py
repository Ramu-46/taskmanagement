from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.employee_list, name='employees'),
    path('tasks/', views.all_tasks, name='all_tasks'),
    path('overdue/', views.overdue_tasks, name='overdue_tasks'),
    path('no-deadline/', views.no_deadline_tasks, name='no_deadline_tasks'),
    path('due-today/', views.due_today_tasks, name='due_today_tasks'),
    path('pending/', views.pending_tasks, name='pending_tasks'),
    path('in-progress/', views.in_progress_tasks, name='in_progress_tasks'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
]
