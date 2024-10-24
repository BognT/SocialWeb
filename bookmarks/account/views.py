from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .forms import (
    LoginForm, 
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
    )


@login_required
def dashboard(request):
    # Defines the dashboard view, which is restricted to authenticated users.
    return render(
        request, 
        'account/dashboard.html', 
        {'section': 'dashboard'}
    )

def user_login(request):
    if request.method == 'POST':
        # Instantiate the form with submitted data
        form = LoginForm(request.POST)

        # Validate the form data
        if form.is_valid():
            cd = form.cleaned_data

            # Authenticate user using the provided credentials
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )

            # If user is authenticated
            if user is not None:
                # Check if the user account is active
                if user.is_active:
                    # Log the user in and return a success message
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    # Return a message if the account is disabled
                    return HttpResponse('Disabled account')
            else:
                # Return a message if the login credentials are invalid
                return HttpResponse('Invalid login')
    else:
        # Instantiate an empty form if the request is GET
        form = LoginForm()

    # Render the login form in the template
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user}
            )
    else:
        user_form = UserRegistrationForm()
    
    return render(
            request,
            'account/register.html', 
            {'user_form': user_form}
        )

def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request, 
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )
