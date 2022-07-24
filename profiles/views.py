from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    '''
    Show the user profile page with form pre-populated with saved info and
    order history list.
    If post request, update the profile with the data from the form.
    '''

    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile information was updated.')
        else:
            messages.error(request, 'Please check the form and submit again.')
    else:
        form = UserProfileForm(instance=user_profile)
    
   
    template = 'profiles/profile.html'
    context = {
        'form': form,
    }

    return render(request, template, context)