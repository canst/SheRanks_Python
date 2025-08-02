from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, F
from django.contrib.auth.decorators import login_required
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .models import University, Post, Rating
from .forms import RatingForm, PostForm

def calculate_post_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(text)
    return vs['compound']

def recalculate_university_ranking(university):
    female_ratings = Rating.objects.filter(university=university, user__profile__gender='female')

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

    university.ranking_score = (
        (university.safety_score * 0.3) +
        (university.inclusivity_score * 0.2) +
        (university.support_score * 0.2) +
        (university.living_score * 0.15) +
        (university.equality_score * 0.15) +
        (university.post_sentiment_score * 0.5)
    )
    
    university.save()

def university_list(request):
    universities = University.objects.all().order_by('-ranking_score')

    # Handle search queries
    query = request.GET.get('q')
    if query:
        universities = universities.filter(name__icontains=query)
        
    # Handle advanced filters
    country = request.GET.get('country')
    min_score = request.GET.get('min_score')
    max_score = request.GET.get('max_score')

    if country:
        universities = universities.filter(location__icontains=country)
    if min_score:
        universities = universities.filter(ranking_score__gte=min_score)
    if max_score:
        universities = universities.filter(ranking_score__lte=max_score)

    # Get a unique list of countries for the filter dropdown
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

    # Handle comment submission
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = get_object_or_404(Post, id=request.POST.get('post_id'))
                comment.author = request.user
                comment.save()
                return redirect('universities:detail', university_slug=university.slug)
    else:
        comment_form = CommentForm()

    posts = Post.objects.filter(university=university).order_by('-created_at')
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

def compare_universities(request, slugs):
    slug_list = slugs.split('/')
    universities = University.objects.filter(slug__in=slug_list)
    
    context = {
        'universities': universities
    }
    return render(request, 'universities/compare_universities.html', context)
