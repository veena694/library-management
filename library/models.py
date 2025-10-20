from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ['first_name', 'last_name']


class ResourceType(models.Model):
    TYPE_CHOICES = [
        ('book', 'Book'),
        ('journal', 'Journal Article'),
        ('thesis', 'Thesis/Dissertation'),
        ('conference', 'Conference Paper'),
        ('digital', 'Digital Resource'),
        ('multimedia', 'Multimedia'),
    ]
    
    name = models.CharField(max_length=50, choices=TYPE_CHOICES, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.get_name_display()


class LibraryResource(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('checked_out', 'Checked Out'),
        ('digital', 'Digital Access'),
        ('restricted', 'Restricted Access'),
    ]
    
    title = models.CharField(max_length=500)
    authors = models.ManyToManyField(Author, related_name='resources')
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='resources')
    
    description = models.TextField()
    abstract = models.TextField(blank=True)
    
    publication_year = models.PositiveIntegerField()
    publisher = models.CharField(max_length=200, blank=True)
    
    isbn = models.CharField(max_length=20, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    
    call_number = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    
    url = models.URLField(blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, default='English')
    
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('library:resource_detail', kwargs={'pk': self.pk})
    
    @property
    def author_names(self):
        return ", ".join([author.full_name for author in self.authors.all()])
    
    @property
    def is_available(self):
        return self.availability in ['available', 'digital']
    
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    class Meta:
        ordering = ['-date_added']


class Keyword(models.Model):
    word = models.CharField(max_length=100, unique=True)
    resources = models.ManyToManyField(LibraryResource, related_name='keywords')
    frequency = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.word
    
    class Meta:
        ordering = ['-frequency', 'word']


class SearchLog(models.Model):
    query = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    results_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-timestamp']


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(LibraryResource, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'resource']
        ordering = ['-date_added']