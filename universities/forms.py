# C:\Users\soyam\Documents\GitHub\SheRanks_Python\universities\forms.py
from django import forms
from .models import Rating, Post
from django.core.exceptions import ValidationError

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
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            raise ValidationError("Only image files (png, jpg, jpeg, gif) are allowed.")

        return image
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }    