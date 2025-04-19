from django.contrib import admin
from .models import Food,WorkoutCategory,Exercise

# Register your models here.
admin.site.register(Food)
admin.site.register(WorkoutCategory)
admin.site.register(Exercise)
