from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('favorites/', views.favorites_view, name='favorites'),
    
    # Main search
    path('', views.LibrarySearchView.as_view(), name='search'),
    
    # Resource details
    path('resource/<int:pk>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    
    # User interactions
    path('favorite/<int:resource_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    # AJAX endpoints
    path('api/keywords/', views.keyword_autocomplete, name='keyword_autocomplete'),
    
    # Statistics
    path('statistics/', views.statistics_view, name='statistics'),
]
