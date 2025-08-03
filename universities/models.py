from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200)
    website = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, help_text="A URL-friendly version of the university name.")
    is_verified = models.BooleanField(default=False, help_text="Has this university been officially verified?")
    # add this field if missing
    rank = models.PositiveIntegerField(null=True, blank=True) 
    num_ratings = models.IntegerField(default=0)
    ranking_score = models.FloatField(default=0.0)
    safety_score = models.FloatField(default=0.0)
    inclusivity_score = models.FloatField(default=0.0)
    support_score = models.FloatField(default=0.0)
    living_score = models.FloatField(default=0.0)
    equality_score = models.FloatField(default=0.0)
    
    post_sentiment_score = models.FloatField(default=0.0) 

    def __str__(self):
        return self.name

class Post(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='uploads/post_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sentiment_score = models.FloatField(default=0.0, help_text="AI-generated sentiment score.")

    def __str__(self):
        return f'{self.title} by {self.author.username}'

    class Meta:
        ordering = ['-created_at']
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    
    safety = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    inclusivity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    support = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    living = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    equality = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'university')

    def __str__(self):
        return f'{self.user.username} rated {self.university.name}'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'