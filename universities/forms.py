# C:\Users\soyam\Documents\GitHub\SheRanks_Python\universities\forms.py
from django import forms
from .models import Rating, Post, Comment # Add Comment to this line

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['safety', 'inclusivity', 'support', 'living', 'equality']
        widgets = {
            'safety': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'inclusivity': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'support': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'living': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'equality': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }
        
class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'location', 'website', 'description']