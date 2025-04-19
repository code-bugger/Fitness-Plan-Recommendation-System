from django.db import models

# Create your models here.
class Food(models.Model):
    FOOD_TYPE_CHOICES = (
        (0, 'Vegetarian'),
        (1, 'Non-Vegetarian'),
    )

    item = models.CharField(max_length=255) 
    calories = models.DecimalField(max_digits=6, decimal_places=2) 
    fats = models.DecimalField(max_digits=5, decimal_places=2) 
    proteins = models.DecimalField(max_digits=5, decimal_places=2)  
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)  
    sugars = models.DecimalField(max_digits=5, decimal_places=2) 
    veg_nonveg = models.IntegerField(choices=FOOD_TYPE_CHOICES) 
    quantity = models.CharField(max_length=100, default="100 gram") 
    breakfast = models.BooleanField(default=False) 
    lunch = models.BooleanField(default=False)  
    dinner = models.BooleanField(default=False) 

    def __str__(self):
        return self.item
    
class WorkoutCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Exercise(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    TARGET_GOAL_CHOICES = [
        ('Weight Gain', 'Weight Gain'),
        ('Weight Loss', 'Weight Loss'),
        ('Healthy', 'Healthy'),
    ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(WorkoutCategory, on_delete=models.CASCADE, related_name='exercises')
    target_goal = models.CharField(max_length=20, choices=TARGET_GOAL_CHOICES)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    equipment_required = models.CharField(max_length=100, null=True, blank=True)
    female_modification = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='workout/', null=True, blank=True)

    def __str__(self):
        return self.name


