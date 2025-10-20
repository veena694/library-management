from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from .models import LibraryResource, Subject, ResourceType, Keyword, SearchLog, UserFavorite, Author
from .forms import LibrarySearchForm, UserRegistrationForm, UserLoginForm


def home(request):
    featured_books = Book.objects.filter(availability='available').order_by('-views')[:6]
    categories = Category.objects.annotate(book_count=Count('books'))[:8]
    recent_books = Book.objects.all()[:8]
    
    context = {
        'featured_books': featured_books,
        'categories': categories,
        'recent_books': recent_books,
        'total_books': Book.objects.count(),
        'total_categories': Category.objects.count(),
    }
    return render(request, 'library/home.html', context)

def search_books(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')
    availability = request.GET.get('availability')
    sort_by = request.GET.get('sort', '-added_date')
    
    books = Book.objects.all()
    
    if query:
        # Advanced keyword-based search
        search_terms = re.findall(r'\w+', query.lower())
        q_objects = Q()
        
        for term in search_terms:
            q_objects |= (
                Q(title__icontains=term) |
                Q(description__icontains=term) |
                Q(keywords__icontains=term) |
                Q(authors__name__icontains=term) |
                Q(publisher__icontains=term)
            )
        
        books = books.filter(q_objects).distinct()
        
        # Save search history
        if request.user.is_authenticated or True:
            SearchHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                query=query,
                results_count=books.count(),
                ip_address=request.META.get('REMOTE_ADDR')
            )
    
    if category_id:
        books = books.filter(category_id=category_id)
    
    if availability:
        books = books.filter(availability=availability)
    
    books = books.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'categories': categories,
        'selected_category': category_id,
        'selected_availability': availability,
        'sort_by': sort_by,
        'total_results': books.count(),
    }
    
    return render(request, 'library/search.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.views += 1
    book.save(update_fields=['views'])
    
    related_books = Book.objects.filter(
        Q(category=book.category) | Q(keywords__icontains=book.keywords[:50])
    ).exclude(pk=book.pk).distinct()[:4]
    
    reviews = book.reviews.all()[:10]
    
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
    
    context = {
        'book': book,
        'related_books': related_books,
        'reviews': reviews,
        'is_favorite': is_favorite,
    }
    return render(request, 'library/book_detail.html', context)

def browse_categories(request):
    categories = Category.objects.annotate(book_count=Count('books'))
    return render(request, 'library/categories.html', {'categories': categories})

def category_books(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.filter(category=category)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'library/category_books.html', {
        'category': category,
        'page_obj': page_obj,
    })

@login_required
def toggle_favorite(request, pk):
    book = get_object_or_404(Book, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    
    return JsonResponse({'status': 'added'})

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('book')
    return render(request, 'library/favorites.html', {'favorites': favorites})

def autocomplete(request):
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    books = Book.objects.filter(
        Q(title__icontains=query) | Q(keywords__icontains=query)
    )[:10]
    
    suggestions = [{'title': book.title, 'id': book.id} for book in books]
    return JsonResponse({'suggestions': suggestions})

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('library:search')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('library:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'library/register.html', {'form': form})


def login_view(request):
    """User login view with option for admin login"""
    if request.user.is_authenticated:
        return redirect('library:search')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        login_type = request.POST.get('login_type', 'user')
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Check if admin login is requested
                if login_type == 'admin':
                    if user.is_staff or user.is_superuser:
                        login(request, user)
                        messages.success(request, f'Welcome back, Admin {username}!')
                        return redirect('admin:index')
                    else:
                        messages.error(request, 'You do not have admin privileges.')
                        return render(request, 'library/login.html', {'form': form})
                else:
                    login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    next_page = request.GET.get('next', 'library:search')
                    return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'library/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout view"""
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye, {username}! You have been logged out.')
    return redirect('library:search')


@login_required
def profile_view(request):
    """User profile view"""
    user = request.user
    favorites = UserFavorite.objects.filter(user=user).select_related('resource')
    recent_searches = SearchLog.objects.filter(user=user).order_by('-timestamp')[:10]
    
    context = {
        'user': user,
        'favorites': favorites,
        'recent_searches': recent_searches,
        'favorites_count': favorites.count(),
    }
    return render(request, 'library/profile.html', context)


@login_required
def favorites_view(request):
    """View user's favorite resources"""
    favorites = UserFavorite.objects.filter(user=request.user).select_related(
        'resource', 'resource__resource_type'
    ).prefetch_related('resource__authors', 'resource__subjects')
    
    # Pagination
    paginator = Paginator(favorites, 20)
    page = request.GET.get('page')
    favorites_page = paginator.get_page(page)
    
    context = {
        'favorites': favorites_page,
        'total_favorites': favorites.count(),
    }
    return render(request, 'library/favorites.html', context)
class LibrarySearchView(ListView):
    model = LibraryResource
    template_name = 'library/search.html'
    context_object_name = 'resources'
    paginate_by = 20
    
    def get_queryset(self):
        form = LibrarySearchForm(self.request.GET)
        queryset = LibraryResource.objects.select_related('resource_type').prefetch_related(
            'authors', 'subjects', 'keywords'
        )
        
        if form.is_valid():
            query = form.cleaned_data.get('query', '').strip()
            resource_type = form.cleaned_data.get('resource_type')
            subject = form.cleaned_data.get('subject')
            year_range = form.cleaned_data.get('year_range')
            availability = form.cleaned_data.get('availability')
            sort_by = form.cleaned_data.get('sort_by', 'relevance')
            
            # Keyword search
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(abstract__icontains=query) |
                    Q(authors__first_name__icontains=query) |
                    Q(authors__last_name__icontains=query) |
                    Q(keywords__word__icontains=query)
                ).distinct()
                
                # Log search
                SearchLog.objects.create(
                    query=query,
                    user=self.request.user if self.request.user.is_authenticated else None,
                    results_count=queryset.count()
                )
            
            # Apply filters
            if resource_type:
                queryset = queryset.filter(resource_type=resource_type)
            
            if subject:
                queryset = queryset.filter(subjects=subject)
            
            if year_range:
                if year_range == 'before-2000':
                    queryset = queryset.filter(publication_year__lt=2000)
                else:
                    start_year, end_year = map(int, year_range.split('-'))
                    queryset = queryset.filter(
                        publication_year__gte=start_year,
                        publication_year__lte=end_year
                    )
            
            if availability:
                queryset = queryset.filter(availability=availability)
            
            # Apply sorting
            
            if sort_by and sort_by != 'relevance':
                queryset = queryset.order_by(sort_by)
            else:
                queryset = queryset.order_by('-view_count', '-date_added')
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LibrarySearchForm(self.request.GET)
        context['total_resources'] = LibraryResource.objects.count()
        context['available_resources'] = LibraryResource.objects.filter(
            availability='available'
        ).count()
        context['digital_resources'] = LibraryResource.objects.filter(
            availability='digital'
        ).count()
        context['popular_keywords'] = Keyword.objects.order_by('-frequency')[:10]
        context['results_count'] = self.get_queryset().count()
        
        # Add user favorites if authenticated
        if self.request.user.is_authenticated:
            favorite_ids = UserFavorite.objects.filter(
                user=self.request.user
            ).values_list('resource_id', flat=True)
            context['favorite_ids'] = list(favorite_ids)
        
        return context


class ResourceDetailView(DetailView):
    model = LibraryResource
    template_name = 'library/resource_detail.html'
    context_object_name = 'resource'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_view_count()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Related resources
        context['related_resources'] = LibraryResource.objects.filter(
            subjects__in=self.object.subjects.all()
        ).exclude(pk=self.object.pk).distinct()[:5]
        
        # Check if user has favorited
        if self.request.user.is_authenticated:
            context['is_favorited'] = UserFavorite.objects.filter(
                user=self.request.user,
                resource=self.object
            ).exists()
        
        return context


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, resource_id):
    # Check if user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({
            'favorited': False,
            'message': 'Please login to save favorites',
            'redirect': True,
            'redirect_url': f"{reverse('library:login')}?next={request.path}"
        }, status=401)
    
    try:
        resource = get_object_or_404(LibraryResource, pk=resource_id)
        favorite, created = UserFavorite.objects.get_or_create(
            user=request.user,
            resource=resource
        )
        
        if not created:
            favorite.delete()
            favorited = False
            message = "Removed from favorites"
        else:
            favorited = True
            message = "Added to favorites"
        
        return JsonResponse({
            'favorited': favorited,
            'message': message,
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def keyword_autocomplete(request):
    """Autocomplete for keyword search"""
    term = request.GET.get('term', '').strip()
    
    if len(term) >= 2:
        keywords = Keyword.objects.filter(
            word__icontains=term
        ).order_by('-frequency')[:10]
        
        suggestions = [{'value': kw.word, 'label': f"{kw.word} ({kw.frequency})"} for kw in keywords]
    else:
        suggestions = []
    
    return JsonResponse(suggestions, safe=False)


def statistics_view(request):
    """Dashboard with library statistics"""
    context = {
        'total_resources': LibraryResource.objects.count(),
        'available_resources': LibraryResource.objects.filter(availability='available').count(),
        'digital_resources': LibraryResource.objects.filter(availability='digital').count(),
        'total_authors': Author.objects.count(),
        'total_subjects': Subject.objects.count(),
        'popular_resources': LibraryResource.objects.order_by('-view_count')[:10],
        'recent_searches': SearchLog.objects.order_by('-timestamp')[:10],
        'top_keywords': Keyword.objects.order_by('-frequency')[:20],
    }
    
    return render(request, 'library/statistics.html', context)