from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import Food,WorkoutCategory,Exercise


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

class WorkoutCategoryForm(forms.ModelForm):
    class Meta:
        model = WorkoutCategory
        fields = '__all__'

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'