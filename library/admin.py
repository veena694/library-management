from django.contrib import admin
from .models import Subject, Author, ResourceType, LibraryResource, Keyword, SearchLog, UserFavorite


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'resource_count']
    search_fields = ['name']
    
    def resource_count(self, obj):
        return obj.resources.count()
    resource_count.short_description = 'Resources'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'resource_count']
    search_fields = ['first_name', 'last_name', 'email']
    
    def resource_count(self, obj):
        return obj.resources.count()
    resource_count.short_description = 'Resources'


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ['get_name_display', 'icon']


@admin.register(LibraryResource)
class LibraryResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'publication_year', 'availability', 'view_count']
    list_filter = ['resource_type', 'availability', 'publication_year']
    search_fields = ['title', 'description', 'isbn']
    filter_horizontal = ['authors', 'subjects']


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['word', 'frequency']
    search_fields = ['word']


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ['query', 'user', 'results_count', 'timestamp']
    list_filter = ['timestamp']


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'date_added']