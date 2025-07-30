from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from .models import Profile, Task, Notification, Employee
from .forms import AddEmployeeForm, TaskForm, EmployeeForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# ------------------- Login -------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')


# ------------------- Logout -------------------
def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------- Dashboard -------------------
@login_required
def dashboard(request):
    today = timezone.now().date()

    context = {
        'employee_count': Employee.objects.count(),  # ✅ Fix: use Employee model here
        'task_count': Task.objects.count(),
        'overdue_count': Task.objects.filter(due_date__lt=today, status__in=['pending', 'in_progress']).count(),
        'no_deadline_count': Task.objects.filter(due_date__isnull=True).count(),
        'due_today_count': Task.objects.filter(due_date=today).count(),
        'pending_count': Task.objects.filter(status='pending').count(),
        'in_progress_count': Task.objects.filter(status='in_progress').count(),
        'completed_count': Task.objects.filter(status='completed').count(),
        'notification_count': Notification.objects.filter(user=request.user, is_read=False).count()
    }

    return render(request, 'dashboard/dashboard.html', context)


# ------------------- Create Task -------------------
@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()

            if task.alert_all:
                for user in User.objects.exclude(id=request.user.id):
                    Notification.objects.create(
                        user=user,
                        message=f"A new task '{task.title}' has been created by {request.user.first_name}."
                    )

            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'dashboard/create_task.html', {'form': form})


# ------------------- Manage Users -------------------
@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    users = User.objects.all()
    return render(request, 'dashboard/manage_users.html', {'users': users})


# ------------------- Employee List -------------------
@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'dashboard/employee_list.html', {'employees': employees})


# ------------------- Add or Edit Employee -------------------
@login_required
def add_or_edit_employee(request, pk=None):
    if pk:
        employee = get_object_or_404(Employee, pk=pk)
    else:
        employee = None

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'dashboard/employee_form.html', {'form': form})


# ------------------- Add Employee -------------------
@login_required
def add_employee(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            role = form.cleaned_data['role']
            profile_picture = form.cleaned_data.get('profile_picture')

            if User.objects.filter(email=email).exists():
                form.add_error('email', 'An employee with this email already exists.')
            else:
                # Create the Django User
                random_password = get_random_string(length=10)
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=random_password,
                    first_name=name
                )

                # Create the Profile
                Profile.objects.create(
                    user=user,
                    name=name,
                    phone=phone,
                    role=role,
                    profile_picture=profile_picture,
                    email=email
                )

                # Create the Employee (sync with dashboard count and listing)
                Employee.objects.create(
                    name=name,
                    username=email,
                    email=email,
                    phone=phone,
                    role=role,
                    profile_picture=profile_picture
                )

                # Send welcome email (optional)
                try:
                    send_mail(
                        subject='Welcome to TaskPro',
                        message=(
                            f"Hello {name},\n\n"
                            "Your account has been created. Here are your login credentials:\n\n"
                            f"Username: {email}\n"
                            f"Password: {random_password}\n\n"
                            "Please change your password after logging in."
                        ),
                        from_email=None,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("Email sending failed:", e)

                return redirect('employee_list')
    else:
        form = AddEmployeeForm()

    return render(request, 'dashboard/add_employee.html', {'form': form})


# ------------------- Delete Employee -------------------
@login_required
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employee_list')


# ------------------- All Tasks -------------------
@login_required
def all_tasks(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'dashboard/all_tasks.html', {'tasks': tasks})


# ------------------- View Notifications -------------------
@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications.update(is_read=True)
    return render(request, 'dashboard/notifications.html', {'notifications': notifications})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.is_staff = bool(request.POST.get('is_staff'))
        user.is_superuser = bool(request.POST.get('is_superuser'))
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('manage_users')
    
    return render(request, 'dashboard/edit_user.html', {'user': user})
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('manage_users')

@login_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_staff = bool(request.POST.get('is_staff'))
        is_superuser = bool(request.POST.get('is_superuser'))

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            messages.success(request, 'User added successfully.')
            return redirect('manage_users')

    return render(request, 'dashboard/add_user.html')
