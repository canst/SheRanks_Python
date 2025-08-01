from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import University, Post

class UniversityResource(resources.ModelResource):
    class Meta:
        model = University
        fields = (
            'name', 'location', 'slug', 'website', 'description', 
            'safety_score', 'inclusivity_score', 'support_score',
            'living_score', 'equality_score', 'ranking_score'
        )
        import_id_fields = ('slug',)

@admin.register(University)
class UniversityAdmin(ImportExportModelAdmin):
    resource_class = UniversityResource
    list_display = ('name', 'location', 'ranking_score', 'is_verified')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_verified',)
    search_fields = ('name', 'location')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'university', 'author', 'created_at', 'sentiment_score')
    list_filter = ('created_at', 'university')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'