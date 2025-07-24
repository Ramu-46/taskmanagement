from django.shortcuts import render
from .models import Employee, Task
from datetime import date

def dashboard_view(request):
    employees = Employee.objects.count()
    all_tasks = Task.objects.count()
    overdue = Task.objects.filter(status='overdue').count()
    no_deadline = Task.objects.filter(due_date__isnull=True).count()
    due_today = Task.objects.filter(due_date=date.today()).count()
    notifications = 5  # You can customize this logic
    pending = Task.objects.filter(status='pending').count()
    in_progress = Task.objects.filter(status='in_progress').count()
    completed = Task.objects.filter(status='completed').count()

    context = {
        'employees': employees,
        'all_tasks': all_tasks,
        'overdue': overdue,
        'no_deadline': no_deadline,
        'due_today': due_today,
        'notifications': notifications,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed,
    }
    return render(request, 'dashboard/index.html', context)

