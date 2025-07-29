from django import forms # type: ignore
from .models import Employee, Profile
from .models import Task
<<<<<<< HEAD
from django.contrib.auth.models import User
=======
>>>>>>> 96b7f93918218470afc831e1752c48c59849882d

class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'name', 'email', 'phone', 'role']


<<<<<<< HEAD

class TaskForm(forms.ModelForm):
    assigned_manager = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='manager'),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    assigned_employees = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(profile__role='employee'),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'style': 'width: 100%'}),
        required=False,
        label='Assign Employees'
    )
    
=======
class TaskForm(forms.ModelForm):
>>>>>>> 96b7f93918218470afc831e1752c48c59849882d
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