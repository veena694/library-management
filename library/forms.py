from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import LibraryResource, Subject, ResourceType


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class LibrarySearchForm(forms.Form):
    query = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter keywords, title, author, or subject...',
            'id': 'id_query'
        })
    )
    
    resource_type = forms.ModelChoiceField(
        queryset=ResourceType.objects.all(),
        required=False,
        empty_label="All Resource Types",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label="All Subjects",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    YEAR_CHOICES = [
        ('', 'Any Year'),
        ('2020-2024', '2020-2024'),
        ('2015-2019', '2015-2019'),
        ('2010-2014', '2010-2014'),
        ('2000-2009', '2000-2009'),
        ('before-2000', 'Before 2000'),
    ]
    
    year_range = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    AVAILABILITY_CHOICES = [
        ('', 'All Resources'),
        ('available', 'Available Now'),
        ('digital', 'Digital Access'),
        ('checked_out', 'Checked Out'),
    ]
    
    availability = forms.ChoiceField(
        choices=AVAILABILITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    SORT_CHOICES = [
        ('relevance', 'Relevance'),
        ('title', 'Title A-Z'),
        ('-title', 'Title Z-A'),
        ('-publication_year', 'Newest First'),
        ('publication_year', 'Oldest First'),
        ('-view_count', 'Most Popular'),
        ('-date_added', 'Recently Added'),
    ]
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='relevance',
        widget=forms.Select(attrs={'class': 'form-select'})
    )