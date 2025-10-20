from django.core.management.base import BaseCommand
from library.models import Subject, Author, ResourceType, LibraryResource, Keyword


class Command(BaseCommand):
    help = 'Create minimal test data (10 resources)'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating minimal test data...')
        
        # Create 1 subject
        subject, _ = Subject.objects.get_or_create(
            name='Computer Science',
            defaults={'description': 'Study of computers and computing'}
        )
        
        # Create 1 resource type
        rtype, _ = ResourceType.objects.get_or_create(
            name='book',
            defaults={'icon': 'fas fa-book'}
        )
        
        # Create 2 authors
        author1, _ = Author.objects.get_or_create(
            first_name='John',
            last_name='Doe',
            defaults={'email': 'john@example.com'}
        )
        
        author2, _ = Author.objects.get_or_create(
            first_name='Jane',
            last_name='Smith',
            defaults={'email': 'jane@example.com'}
        )
        
        # Create 10 simple resources
        titles = [
            'Introduction to Python Programming',
            'Web Development with Django',
            'Data Science Fundamentals',
            'Machine Learning Basics',
            'Database Design Principles',
            'Software Testing Guide',
            'Agile Development Practices',
            'Computer Networks Overview',
            'Cloud Computing Essentials',
            'Cybersecurity Introduction',
        ]
        
        for i, title in enumerate(titles):
            resource, created = LibraryResource.objects.get_or_create(
                title=title,
                defaults={
                    'description': f'A comprehensive guide to {title.lower()}.',
                    'abstract': f'This book covers all essential topics in {title.lower()}.',
                    'publication_year': 2020 + (i % 5),
                    'publisher': 'Test Publisher',
                    'isbn': f'978-123456{i:04d}',
                    'call_number': f'QA76.{i+1}',
                    'location': 'Main Library',
                    'availability': 'available' if i % 2 == 0 else 'digital',
                    'pages': 200 + (i * 50),
                    'language': 'English',
                    'resource_type': rtype,
                }
            )
            
            if created:
                # Add authors
                resource.authors.add(author1 if i % 2 == 0 else author2)
                
                # Add subject
                resource.subjects.add(subject)
                
                # Add keywords
                keywords = ['programming', 'technology', 'learning', 'guide']
                for kw in keywords[:2+i%3]:
                    keyword, _ = Keyword.objects.get_or_create(
                        word=kw,
                        defaults={'frequency': 1}
                    )
                    keyword.resources.add(resource)
                
                self.stdout.write(f'✓ Created: {title}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Created {len(titles)} test resources successfully!'
            )
        )