# C:\Users\soyam\Documents\GitHub\SheRanks_Python\universities\views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, F
from django.contrib.auth.decorators import login_required
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .models import University, Post, Rating
from .forms import RatingForm, PostForm

# This function calculates the sentiment of a post
def calculate_post_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    return vs['compound']

# This function recalculates the university's scores and ranking based on ALL data
def recalculate_university_ranking(university):
    # 1. Get average scores from female ratings
    female_ratings = Rating.objects.filter(university=university, user__profile__gender='female')
    if female_ratings.exists():
        avg_scores = female_ratings.aggregate(
            avg_safety=Avg('safety'),
            avg_inclusivity=Avg('inclusivity'),
            avg_support=Avg('support'),
            avg_living=Avg('living'),
            avg_equality=Avg('equality'),
        )
        university.safety_score = avg_scores['avg_safety'] if avg_scores['avg_safety'] is not None else 0.0
        university.inclusivity_score = avg_scores['avg_inclusivity'] if avg_scores['avg_inclusivity'] is not None else 0.0
        university.support_score = avg_scores['avg_support'] if avg_scores['avg_support'] is not None else 0.0
        university.living_score = avg_scores['avg_living'] if avg_scores['avg_living'] is not None else 0.0
        university.equality_score = avg_scores['avg_equality'] if avg_scores['avg_equality'] is not None else 0.0
    else:
        university.safety_score = 0.0
        university.inclusivity_score = 0.0
        university.support_score = 0.0
        university.living_score = 0.0
        university.equality_score = 0.0

    # 2. Get average sentiment from all posts (AI analysis)
    all_posts = Post.objects.filter(university=university)
    if all_posts.exists():
        avg_sentiment = all_posts.aggregate(avg_score=Avg('sentiment_score'))['avg_score']
        university.post_sentiment_score = avg_sentiment if avg_sentiment is not None else 0.0
    else:
        university.post_sentiment_score = 0.0

    # 3. Calculate the final ranking score (composite of ratings and post sentiment)
    # VADER's compound score ranges from -1 to 1. We scale it to fit our ranking scale.
    # We'll give it a small weight to influence the score.
    university.ranking_score = (
        (university.safety_score * 0.3) +
        (university.inclusivity_score * 0.2) +
        (university.support_score * 0.2) +
        (university.living_score * 0.15) +
        (university.equality_score * 0.15) +
        (university.post_sentiment_score * 0.5) # Adding post sentiment with a small weight
    )
    
    university.save()

# Standard views
def university_list(request):
    universities = University.objects.all().order_by('-ranking_score')
    query = request.GET.get('q')
    if query:
        universities = universities.filter(name__icontains=query)
    context = {
        'universities': universities,
        'search_query': query,
    }
    return render(request, 'universities/university_list.html', context)

def university_detail(request, university_slug):
    university = get_object_or_404(University, slug=university_slug)
    all_universities = list(University.objects.all().order_by('-ranking_score'))
    try:
        rank = all_universities.index(university) + 1
    except ValueError:
        rank = "N/A"
    # Order posts by created_at in descending order
    posts = Post.objects.filter(university=university).order_by('-created_at')
    context = {
        'university': university,
        'posts': posts,
        'rank': rank,
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
            # AI analysis of post content
            post.sentiment_score = calculate_post_sentiment(post.content)
            post.save()
            
            # Recalculate university ranking after a new post is made
            recalculate_university_ranking(university)
            
            return redirect('universities:detail', university_slug=university.slug)
    else:
        form = PostForm()
    
    return render(request, 'universities/create_post.html', {'form': form, 'university': university})

@login_required
def rate_university(request, university_slug):
    university = get_object_or_404(University, slug=university_slug)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.university = university
            rating.save()
            
            recalculate_university_ranking(university)

            return redirect('universities:detail', university_slug=university.slug)
    else:
        form = RatingForm()
    
    return render(request, 'universities/rate_university.html', {'form': form, 'university': university})