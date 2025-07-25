from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date
from .models import Profile, Task
from .forms import AddEmployeeForm


# ------------------- Login View -------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')


# ------------------- Logout View -------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------- Dashboard View -------------------
@login_required
def dashboard(request):
    context = {
        'employees': User.objects.filter(is_superuser=False).count(),
        'all_tasks': Task.objects.count(),
        'overdue': Task.objects.filter(due_date__lt=date.today(), status__in=['pending', 'in_progress']).count(),
        'no_deadline': Task.objects.filter(due_date__isnull=True).count(),
        'due_today': Task.objects.filter(due_date=date.today()).count(),
        'notifications': 0,  # Placeholder
        'pending': Task.objects.filter(status='pending').count(),
        'in_progress': Task.objects.filter(status='in_progress').count(),
        'completed': Task.objects.filter(status='completed').count(),
    }
    return render(request, 'dashboard/dashboard.html', context)


# ------------------- Create Task View -------------------
@login_required
def create_task(request):
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            due_date=request.POST['due_date'],
            status=request.POST['status'],
            assigned_by=request.user
        )
        return redirect('dashboard')
    return render(request, 'dashboard/create_task.html')


# ------------------- Manage Users View (Admin Only) -------------------
@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    users = User.objects.all()
    return render(request, 'dashboard/manage_users.html', {'users': users})


# ------------------- Employees List View -------------------
@login_required
def employee_list(request):
    employees = User.objects.filter(is_superuser=False)
    return render(request, 'dashboard/employee_list.html', {'employees': employees})


# ------------------- Add New Employee View -------------------
@login_required
def add_employee(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(User.objects.make_random_password())  # or let user set their password
            user.save()
            form.save_profile(user)
            return redirect('employee_list')
    else:
        form = AddEmployeeForm()
    return render(request, 'dashboard/add_employee.html', {'form': form})
