from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from universities.models import University

from .models import Profile  
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Create profile if it doesn't exist to avoid duplicates
            Profile.objects.get_or_create(user=user)
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    universities = University.objects.all().order_by('name')
    context = {
        'form': form,
        'universities': universities
    }
    return render(request, 'registration/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        universities = University.objects.all().order_by('name')

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'universities': universities
    }
    return render(request, 'registration/profile.html', context)