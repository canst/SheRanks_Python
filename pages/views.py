# C:\Users\soyam\Documents\GitHub\SheRanks_Python\pages\views.py
from django.shortcuts import render
from universities.models import University, Post, Rating
from django.db.models import Avg, F

def home(request):
    top_ranked_universities = University.objects.all().order_by('-ranking_score')[:20]

    context = {
        'top_ranked_universities': top_ranked_universities,
        'mission_statement': "Our mission is to create a safe and inclusive environment where all female students can thrive academically and personally...",
        'team_members': [
            {
                'name': 'Looking for Contributors',
                'role': 'Team member 1',
                'avatar': 'images/team/team_sophia.jpg',
                'linkedin': 'https://linkedin.com/',
                'x_url': 'https://x.com',
            },
            {
                'name': 'Yao Amevi A. Sossou',
                'role': 'Lead Developer',
                'avatar': 'images/team/IMG-20250714-WA0024.jpg',
                'linkedin': 'https://linkedin.com/in/ameviy',
                'x_url': 'https://x.com/_amevY2',
            },
            {
                'name': 'Looking for Contributors',
                'role': 'Team member 2',
                'avatar': 'images/team/Join.jpg',
                'linkedin': 'https://linkedin.com',
                'x_url': 'https://x.com',
            },
        ],
        'call_to_action': "Join us in our mission to rank universities on gender equality and safety. Register or post your experience today!",
        'donation_link': "#",
    }
    return render(request, 'pages/home.html', context)

def methodology_page(request):
    data = {
        'labels': ['Safety', 'Inclusivity', 'Support', 'Living', 'Equality'],
        'values': [4.5, 4.2, 4.0, 3.8, 4.1],
        'outcomes': {
            'categories': ['Awareness', 'Action', 'Policy Change'],
            'values': [65, 80, 45]
        }
    }
    return render(request, 'pages/methodology.html', {'data': data})