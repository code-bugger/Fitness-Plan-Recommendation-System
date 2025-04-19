from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Package, Booking
from .forms import PackageForm, BookingForm


def is_admin(user):
    return user.is_superuser


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(request, "You are not allowed to access this page.")
            return HttpResponseRedirect(reverse('packages'))
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='login')
def packages(request):
    active_packages = Package.objects.filter(is_active=True)
    allpackages = Package.objects.all()
    return render(request, 'packages/package_list.html', {'packages': allpackages,'active_packages':active_packages})


@login_required(login_url='login')
@admin_required
def package_create(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save()
            messages.success(request, f"Package '{package.name}' created successfully!")
            return redirect('packages')
    else:
        form = PackageForm()
    return render(request, 'packages/package_form.html', {'form': form})


@login_required(login_url='login')
@admin_required
def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, 'packages/package_detail.html', {'package': package})


@login_required(login_url='login')
@admin_required
def package_update(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, f"Package '{package.name}' updated successfully!")
            return redirect('packages')
    else:
        form = PackageForm(instance=package)
    return render(request, 'packages/package_form.html', {'form': form})


@login_required(login_url='login')
@admin_required
def package_delete(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        package_name = package.name
        package.delete()
        messages.success(request, f"Package '{package_name}' deleted successfully!")
        return redirect('packages')
    return render(request, 'packages/package_confirm_delete.html', {'package': package})


@login_required(login_url='login')
def book_membership(request, package_id):
    package = get_object_or_404(Package, id=package_id, is_active=True)

    existing_booking = Booking.objects.filter(user=request.user, membership_package=package, status='Pending').first()

    if existing_booking:
        messages.warning(request, f"You already have a pending booking for the '{package.name}' package.")
        return redirect('packages')

    if request.method == 'POST':
        Booking.objects.create(
            user=request.user,
            membership_package=package,
            status='Pending'
        )
        messages.success(request, f"You have successfully booked the '{package.name}' package. Your booking is pending approval.")
        return redirect('packages')

    return render(request, 'bookings/book_membership.html', {'package': package})


@login_required(login_url='login')
@admin_required
def booking_list(request):
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = Booking.objects.filter(status=status_filter)
    else:
        bookings = Booking.objects.all()
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required(login_url='login')
@admin_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required(login_url='login')
@admin_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, f"Booking for the '{booking.membership_package.name}' package updated successfully!")
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'bookings/booking_form.html', {'form': form})


@login_required(login_url='login')
@admin_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking_package_name = booking.membership_package.name
        booking.delete()
        messages.success(request, f"Booking for the '{booking_package_name}' package deleted successfully!")
        return redirect('booking_list')
    return render(request, 'bookings/booking_confirm_delete.html', {'booking': booking})
