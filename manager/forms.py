from django import forms
from .models import Task, TaskType, Position, Worker


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees", "is_completed"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "assignees": forms.CheckboxSelectMultiple(),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["username", "first_name", "last_name", "email", "position"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-select"}),
        }
