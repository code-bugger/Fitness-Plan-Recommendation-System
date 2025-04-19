from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate,login,logout
from .forms import UserRegistrationForm,FoodForm,WorkoutCategoryForm,ExerciseForm
from django.contrib.auth.decorators import login_required
from .models import Food,WorkoutCategory,Exercise
from membership.models import Package, Booking
from django.contrib.auth.models import User


from recommender.functions import calculate_required_calories,recommend_diet,recommend_workout

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def recommendation(request):
    if request.method == 'POST':
        # Get user input from form
        age = int(request.POST['age'])
        weight = float(request.POST['weight'])
        height = float(request.POST['height'])
        gender = request.POST.get('gender', 'Male')  # Provide a default value
        activity = request.POST.get('activity', '1.2')  # Provide a default value
        diet_preference = 'veg' if request.POST['veg_nonveg'] == '0' else 'non-veg'
        goal = request.POST.get('goal', 'Maintain')  # Provide a default value

        # Calculate required daily calories for the user
        required_calories = calculate_required_calories(age, weight, height, gender, activity, goal)

        # Calculate calorie distribution for meals
        breakfast_calories = required_calories * 0.25
        lunch_calories = required_calories * 0.40
        dinner_calories = required_calories * 0.35

        # Get recommended diets for breakfast, lunch, and dinner
        breakfast_foods, breakfast_total = recommend_diet(breakfast_calories, 'breakfast', goal, diet_preference)
        lunch_foods, lunch_total = recommend_diet(lunch_calories, 'lunch', goal, diet_preference)
        dinner_foods, dinner_total = recommend_diet(dinner_calories, 'dinner', goal, diet_preference)

        total_calories = breakfast_total + lunch_total + dinner_total

        # Get the recommended workout plan
        workout_plan = recommend_workout(age, gender, height, weight, goal)

        # Pass data to the template for rendering
        context = {
            'required_calories': required_calories,
            'breakfast_foods': breakfast_foods,
            'breakfast_total': breakfast_total,
            'lunch_foods': lunch_foods,
            'lunch_total': lunch_total,
            'dinner_foods': dinner_foods,
            'dinner_total': dinner_total,
            'total_calories': total_calories,
            'workout_plan': workout_plan
        }
        return render(request, 'results.html', context)

    # If GET request, just render the form
    return render(request, 'user_form.html')


def registerPage(request):
    form=UserRegistrationForm()

    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        
    return render(request, 'accounts/register.html',{'form':form})

def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username OR Password is incorrect')

    return render(request, 'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')


def is_admin(user):
    return user.is_superuser

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(request, "You are not allowed to access this page.")
            return HttpResponseRedirect(reverse('home'))
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required(login_url='login')
@admin_required
def dashboard(request):
    context = {
        'foodCount': Food.objects.count(),
        'exerciseCount': Exercise.objects.count(),
        'userCount': User.objects.count(),
        'memberCount': Booking.objects.count(),
        'packageCount': Package.objects.count(),
    }
    return render(request, 'dashboard.html', context)

# CRUD Views for Food
@login_required(login_url='login')
@admin_required
def food_list(request):
    foods = Food.objects.all()
    return render(request, 'foods/food_list.html', {'foods': foods})

@login_required(login_url='login')
@admin_required
def food_create(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save()
            messages.success(request, f"Food item '{food.item}' created successfully!")
            return redirect('food_list')
    else:
        form = FoodForm()
    return render(request, 'foods/food_form.html', {'form': form})

@login_required(login_url='login')
@admin_required
def food_edit(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            messages.success(request, f"Food item '{food.item}' updated successfully!")
            return redirect('food_list')
    else:
        form = FoodForm(instance=food)
    return render(request, 'foods/food_form.html', {'form': form})

@login_required(login_url='login')
@admin_required
def food_delete(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == 'POST':
        food_name = food.item
        food.delete()
        messages.success(request, f"Food item '{food_name}' deleted successfully!")
        return redirect('food_list')
    return render(request, 'foods/food_confirm_delete.html', {'food': food})

# CRUD Views for WorkoutCategory
@login_required(login_url='login')
@admin_required
def category_list(request):
    categories = WorkoutCategory.objects.all()
    return render(request, 'workout/category_list.html', {'categories': categories})

@login_required(login_url='login')
@admin_required
def category_create(request):
    if request.method == 'POST':
        form = WorkoutCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created successfully!")
            return redirect('category_list')
    else:
        form = WorkoutCategoryForm()
    return render(request, 'workout/category_form.html', {'form': form})

@login_required(login_url='login')
@admin_required
def category_update(request, pk):
    category = get_object_or_404(WorkoutCategory, pk=pk)
    if request.method == 'POST':
        form = WorkoutCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated successfully!")
            return redirect('category_list')
    else:
        form = WorkoutCategoryForm(instance=category)
    return render(request, 'workout/category_form.html', {'form': form})

@login_required(login_url='login')
@admin_required
def category_delete(request, pk):
    category = get_object_or_404(WorkoutCategory, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f"Category '{category_name}' deleted successfully!")
        return redirect('category_list')
    return render(request, 'workout/category_confirm_delete.html', {'category': category})

# CRUD Views for Exercise
@login_required(login_url='login')
@admin_required
def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'workout/exercise_list.html', {'exercises': exercises})

@login_required(login_url='login')
@admin_required
def exercise_create(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            exercise = form.save()
            messages.success(request, f"Exercise '{exercise.name}' created successfully!")
            return redirect('exercise_list')
    else:
        form = ExerciseForm()
    return render(request, 'workout/exercise_form.html', {'form': form})

@login_required(login_url='login')
@admin_required
def exercise_update(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES, instance=exercise)
        if form.is_valid():
            form.save()
            messages.success(request, f"Exercise '{exercise.name}' updated successfully!")
            return redirect('exercise_list')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'workout/exercise_form.html', {'form': form})

@login_required(login_url='login')
@admin_required
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    return render(request, 'workout/exercise_detail.html', {'exercise': exercise})

@login_required(login_url='login')
@admin_required
def exercise_delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        exercise_name = exercise.name
        exercise.delete()
        messages.success(request, f"Exercise '{exercise_name}' deleted successfully!")
        return redirect('exercise_list')
    return render(request, 'workout/exercise_confirm_delete.html', {'exercise': exercise})