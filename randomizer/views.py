from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from .forms import ProfileForm, BaseProfileFormSet
from .models import Profile

def list(request):
    profiles = Profile.objects.all()
    return render(request, 'randomizer/list.html', {'profiles': profiles})


def new(request): 

    # Create the formset, specifying the form and formset we want to use.
    ProfileFormSet = formset_factory(ProfileForm, formset=BaseProfileFormSet)

    if request.method == 'POST':
        profile_formset = ProfileFormSet(request.POST)
        if profile_formset.is_valid():
            # Now save the data for each form in the formset
            new_profiles = []
            for profile_form in profile_formset:
                if profile_form.cleaned_data.get('name'):
                    name = profile_form.cleaned_data.get('name')
                    if name:
                        new_profiles.append(Profile(name=name))
                else:
                    messages.error(request, 'Please, fill the form.')
                    return redirect(reverse('new'))
            # at least one form
            if (profile_formset.forms):
                # create objects
                Profile.objects.bulk_create(new_profiles)
                # And notify our users that it worked

                messages.success(request, 'You have added new names.')
                return redirect('list')
            else:
                messages.error(request, 'Please, fill the form.')
                return redirect(reverse('new'))
        # duplicate case
        else:
            if profile_formset.non_form_errors():
                messages.error(request, profile_formset.non_form_errors()[0])
                return redirect(reverse('new'))
    else:
        profile_formset = ProfileFormSet()

    context = {
        'profile_formset': profile_formset,
    }
    return render(request, 'randomizer/add_names.html', context)

def delete_profile(request, name):
    profile_to_delete = get_object_or_404(Profile, name=name)
    profile_to_delete.delete()

    if request.is_ajax():
        return JsonResponse({
            'status': 'success',
        })
    return redirect('list') 

def get_winners(request):
    winners = []

    for i in range(3):
        random_profile = Profile.objects.random()
        winners.append(random_profile)

    return render(request, 'randomizer/winners.html', {'winners': winners})


def get_another(request):
    random_profile = Profile.objects.random()
    return JsonResponse({
        'name': random_profile.name
    })
