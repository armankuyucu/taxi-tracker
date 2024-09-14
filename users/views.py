from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm
from taxi_tracker.models import Car


def register(request):
    """
    Register a new user and assign cars to the user
    :param request: HttpRequest object
    :return: HttpResponse object with the registration form or redirect to the login page
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            selected_car_ids = request.POST.getlist('cars')

            try:
                # Use a transaction to ensure no user is saved if car assignment fails
                with transaction.atomic():
                    user = form.save()

                    # Check for car assignments
                    for car_id in selected_car_ids:
                        if Car.objects.filter(car_id=car_id).exists():
                            raise IntegrityError(f"Car ID {car_id} is already assigned to another user.")

                        # Create and save the car for the new user
                        car = Car(user=user, car_id=car_id)
                        car.save()

                    messages.success(request, 'Account has been created! Now you can log in.')
                    return redirect('login')

            except IntegrityError as e:
                # Handle the case where car assignment fails, e.g. car ID already assigned to another user
                form.add_error(None, str(e))
                messages.error(request, f"Failed to register user: {e}")
                return render(request, 'users/register.html', {'form': CustomUserCreationForm()})
    else:
        return render(request, 'users/register.html', {'form': CustomUserCreationForm()})


@login_required
def profile(request):
    return render(request, "users/profile.html")
