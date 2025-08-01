from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit)
        user_profile = Profile.objects.get(user=user)
        user_profile.gender = self.cleaned_data['gender']
        user_profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'gender']
        widgets = {
            'gender': forms.RadioSelect(choices=Profile.GENDER_CHOICES)
        }