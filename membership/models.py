from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Package(models.Model):
    PACKAGE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Semi-Annually', 'Semi-Annually'),
        ('Annually', 'Annually'),
    ]

    CATEGORY_CHOICES = [
        ('Individual', 'Individual'),
        ('Student', 'Student'),
        ('Couple', 'Couple'),
        ('Family', 'Family'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    package_type = models.CharField(max_length=20, choices=PACKAGE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Individual')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, related_name='memberships', on_delete=models.CASCADE)
    membership_package = models.ForeignKey(Package, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.membership_package.name} ({self.status})"

