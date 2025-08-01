from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, F
from django.contrib.auth.decorators import login_required
from .models import University, Post, Rating
from .forms import RatingForm, PostForm


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

    posts = university.posts.all()
    context = {
        'university': university,
        'posts': posts,
        'rank': rank,
    }
    return render(request, 'universities/university_detail.html', context)

def calculate_university_scores(university):
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
        
        university.ranking_score = (
            university.safety_score * 0.3 +
            university.inclusivity_score * 0.2 +
            university.support_score * 0.2 +
            university.living_score * 0.15 +
            university.equality_score * 0.15
        )
        university.save()
    else:
        university.safety_score = 0.0
        university.inclusivity_score = 0.0
        university.support_score = 0.0
        university.living_score = 0.0
        university.equality_score = 0.0
        university.ranking_score = 0.0
        university.save()

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
            
            calculate_university_scores(university)

            return redirect('universities:detail', university_slug=university.slug)
    else:
        form = RatingForm()
    
    return render(request, 'universities/rate_university.html', {'form': form, 'university': university})


@login_required
def create_post(request, university_slug):
    university = get_object_or_404(University, slug=university_slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.university = university
            post.author = request.user
            post.save()
            return redirect('universities:detail', university_slug=university.slug)
    else:
        form = PostForm()

    return render(request, 'universities/create_post.html', {'form': form, 'university': university})