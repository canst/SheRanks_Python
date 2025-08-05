# C:\Users\soyam\Documents\GitHub\SheRanks_Python\universities\views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, F, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from rest_framework import viewsets
from .models import University, Post, Rating, Comment # Add Comment
from .forms import RatingForm, PostForm, CommentForm, UniversityForm

def calculate_post_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    return vs['compound']

def recalculate_university_ranking(university):
    # Get average scores from female ratings
    female_ratings = Rating.objects.filter(university=university, user__profile__gender='female')

    rating_count = female_ratings.aggregate(count=Count('id'))['count'] or 0
    university.num_ratings = rating_count

    if female_ratings.exists():
        avg_scores = female_ratings.aggregate(
            avg_safety=Avg('safety'),
            avg_inclusivity=Avg('inclusivity'),
            avg_support=Avg('support'),
            avg_living=Avg('living'),
            avg_equality=Avg('equality'),
        )
        university.safety_score = avg_scores['avg_safety'] or 0.0
        university.inclusivity_score = avg_scores['avg_inclusivity'] or 0.0
        university.support_score = avg_scores['avg_support'] or 0.0
        university.living_score = avg_scores['avg_living'] or 0.0
        university.equality_score = avg_scores['avg_equality'] or 0.0
    else:
        university.safety_score = 0.0
        university.inclusivity_score = 0.0
        university.support_score = 0.0
        university.living_score = 0.0
        university.equality_score = 0.0

    all_posts = Post.objects.filter(university=university)
    if all_posts.exists():
        avg_sentiment = all_posts.aggregate(avg_score=Avg('sentiment_score'))['avg_score']
        university.post_sentiment_score = avg_sentiment if avg_sentiment is not None else 0.0
    else:
        university.post_sentiment_score = 0.0

    rating_weight = min(university.num_ratings / 10.0, 1.0)
    
    score_from_ratings = (
        university.safety_score * 0.3 +
        university.inclusivity_score * 0.2 +
        university.support_score * 0.2 +
        university.living_score * 0.15 +
        university.equality_score * 0.15
    )
    
    university.ranking_score = (score_from_ratings * rating_weight) + (university.post_sentiment_score * 0.2)
    
    university.save()

def university_list(request):
    universities = University.objects.all().order_by('-ranking_score')
    query = request.GET.get('q')
    if query:
        universities = universities.filter(name__icontains=query)
    country = request.GET.get('country')
    min_score = request.GET.get('min_score')
    max_score = request.GET.get('max_score')

    if country:
        universities = universities.filter(location__icontains=country)
    if min_score:
        universities = universities.filter(ranking_score__gte=min_score)
    if max_score:
        universities = universities.filter(ranking_score__lte=max_score)

    countries = sorted(list(University.objects.values_list('location', flat=True).distinct()))

    context = {
        'universities': universities,
        'search_query': query,
        'countries': countries,
        'selected_country': country,
        'min_score': min_score,
        'max_score': max_score,
    }
    return render(request, 'universities/university_list.html', context)

def university_detail(request, university_slug):
    university = get_object_or_404(University, slug=university_slug)
    all_universities = list(University.objects.all().order_by('-ranking_score'))
    try:
        rank = all_universities.index(university) + 1
    except ValueError:
        rank = "N/A"
    posts = Post.objects.filter(university=university).order_by('-created_at')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = get_object_or_404(Post, id=request.POST.get('post_id'))
                comment.author = request.user
                comment.save()
                messages.success(request, 'Your comment has been added!')
                return redirect('universities:detail', university_slug=university.slug)
    else:
        comment_form = CommentForm()

    context = {
        'university': university,
        'posts': posts,
        'rank': rank,
        'comment_form': comment_form,
    }
    return render(request, 'universities/university_detail.html', context)

@login_required
def create_post(request, university_slug):
    university = get_object_or_404(University, slug=university_slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.university = university
            post.author = request.user
            post.sentiment_score = calculate_post_sentiment(post.content)
            post.save()
            
            recalculate_university_ranking(university)
            
            return redirect('universities:detail', university_slug=university.slug)
    else:
        form = PostForm()
    
    return render(request, 'universities/create_post.html', {'form': form, 'university': university})

@login_required
def rate_university(request, university_slug):
    university = get_object_or_404(University, slug=university_slug)
    
    existing_rating = Rating.objects.filter(user=request.user, university=university).first()

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=existing_rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.university = university
            rating.save()
            
            recalculate_university_ranking(university)
            messages.success(request, "Your rating has been updated successfully!")
            return redirect('universities:detail', university_slug=university.slug)
    else:
        form = RatingForm(instance=existing_rating)

    context = {
        'form': form,
        'university': university,
        'existing_rating': existing_rating,
    }
    return render(request, 'universities/rate_university.html', context)
    
def compare_universities(request, slugs):
    slug_list = slugs.split('/')
    universities = University.objects.filter(slug__in=slug_list)
    
    context = {
        'universities': universities
    }
    return render(request, 'universities/compare_universities.html', context)

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer