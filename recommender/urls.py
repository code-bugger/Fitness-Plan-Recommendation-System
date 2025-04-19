from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('recommendation', views.recommendation, name='recommendation'),
    path("login/",views.loginPage,name="login"),
    path("register/",views.registerPage,name="register"),
    path("logout/",views.logoutUser,name="logout"),
    path("dashboard/",views.dashboard,name="dashboard"),

    path('food/', views.food_list, name='food_list'), 
    path('food/create/', views.food_create, name='food_create'), 
    path('food/edit/<int:pk>/', views.food_edit, name='food_edit'), 
    path('food/delete/<int:pk>/', views.food_delete, name='food_delete'),

     # WorkoutCategory CRUD
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    # Exercise CRUD
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/create/', views.exercise_create, name='exercise_create'),
    path('exercises/update/<int:pk>/', views.exercise_update, name='exercise_update'),
    path('exercises/delete/<int:pk>/', views.exercise_delete, name='exercise_delete'),
    path('exercises/<int:pk>/', views.exercise_detail, name='exercise_detail'),
]