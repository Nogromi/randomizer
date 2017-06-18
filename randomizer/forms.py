from django import forms
from django.forms.formsets import BaseFormSet


from django.forms import formset_factory
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name',)

    # name = forms.CharField(
    #     max_length=100,
    #     widget=forms.TextInput(attrs={
    #         'placeholder': ' Name',
    #     }), required=True)


class BaseProfileFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two profiles have the same name.
        """
        # if any(self.errors):
        #     return

        names = []
        urls = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']

                # Check that no two profiles have the same names
                if name:
                    if name in names:
                        duplicates = True
                    names.append(name)

                if duplicates:

                    raise forms.ValidationError(
                        'Profiles must have unique names.',
                        code='duplicate_names'
                    )
