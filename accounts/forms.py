from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from universities.models import University
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    # User Model Fields
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    # Profile Model Fields
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, widget=forms.RadioSelect)
    avatar = forms.ImageField(required=False)
    university_name = forms.CharField(label="University Name", required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    location = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match.")
        
        avatar = cleaned_data.get('avatar')
        if avatar and not avatar.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise forms.ValidationError("Only image files (png, jpg, jpeg, gif) are allowed.")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        
        profile = Profile.objects.create(
            user=user,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            gender=self.cleaned_data.get('gender'),
            birth_date=self.cleaned_data.get('birth_date'),
            avatar=self.cleaned_data.get('avatar'),
            bio=self.cleaned_data.get('bio', ''),
            location=self.cleaned_data.get('location', '')
        )

        university_name = self.cleaned_data.get('university_name')
        if university_name:
            university, created = University.objects.get_or_create(
                name=university_name,
                defaults={'slug': university_name.lower().replace(' ', '-')}
            )
            profile.university = university
            profile.save()

        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    university_name = forms.CharField(label="University Name", required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender', 'birth_date', 'avatar', 'bio', 'location']
        widgets = {
            'gender': forms.RadioSelect(choices=Profile.GENDER_CHOICES),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.university:
            self.initial['university_name'] = self.instance.university.name