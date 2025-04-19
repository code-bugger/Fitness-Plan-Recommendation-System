from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.packages, name='packages'),
    path('package/new/', views.package_create, name='package_create'),
    path('package/<int:pk>/', views.package_detail, name='package_detail'),
    path('package/<int:pk>/edit/', views.package_update, name='package_update'),
    path('package/<int:pk>/delete/', views.package_delete, name='package_delete'),
    path('book-membership/<int:package_id>/', views.book_membership, name='book_membership'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:pk>/edit/', views.booking_update, name='booking_update'),
    path('bookings/<int:pk>/delete/', views.booking_delete, name='booking_delete'), 
]