from django import forms
from .models import Employee, Profile

class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'name', 'email', 'phone', 'role']
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'alert_all']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=[
                ('pending', 'Pending'),
                ('in_progress', 'In Progress'),
                ('completed', 'Completed'),
            ]),
        }
        labels = {
            'alert_all': 'Alert All Employees'
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'