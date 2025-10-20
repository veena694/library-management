from django.core.management.base import BaseCommand
from library.models import (
    Subject, Author, ResourceType, LibraryResource, Keyword
)
import random


class Command(BaseCommand):
    help = 'Populate database with sample library resources'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of resources to create (default: 50)'
        )
    
    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Create Resource Types
        self.stdout.write('Creating resource types...')
        resource_types_data = [
            ('book', 'fas fa-book'),
            ('journal', 'fas fa-newspaper'),
            ('thesis', 'fas fa-graduation-cap'),
            ('conference', 'fas fa-users'),
            ('digital', 'fas fa-laptop'),
            ('multimedia', 'fas fa-video'),
        ]
        
        for type_name, icon in resource_types_data:
            ResourceType.objects.get_or_create(
                name=type_name,
                defaults={'icon': icon}
            )
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(resource_types_data)} resource types'))
        
        # Create Subjects
        self.stdout.write('Creating subjects...')
        subjects_data = [
            ('Computer Science', 'Study of computational systems and algorithms'),
            ('Literature', 'Written works of artistic merit'),
            ('History', 'Study of past events'),
            ('Science', 'Systematic study of the natural world'),
            ('Medicine', 'Science of diagnosis and treatment'),
            ('Engineering', 'Application of science to solve problems'),
            ('Arts', 'Creative and aesthetic expression'),
            ('Philosophy', 'Study of fundamental questions'),
            ('Psychology', 'Scientific study of mind and behavior'),
            ('Economics', 'Study of production and consumption'),
            ('Mathematics', 'Study of numbers and patterns'),
            ('Physics', 'Study of matter and energy'),
            ('Chemistry', 'Study of substances and reactions'),
            ('Biology', 'Study of living organisms'),
            ('Sociology', 'Study of human society'),
        ]
        
        for name, description in subjects_data:
            Subject.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(subjects_data)} subjects'))
        
        # Create Authors
        self.stdout.write('Creating authors...')
        authors_data = [
            ('John', 'Smith', 'john.smith@example.com'),
            ('Maria', 'Garcia', 'maria.garcia@example.com'),
            ('David', 'Johnson', 'david.johnson@example.com'),
            ('Sarah', 'Brown', 'sarah.brown@example.com'),
            ('Michael', 'Davis', 'michael.davis@example.com'),
            ('Lisa', 'Wilson', 'lisa.wilson@example.com'),
            ('Robert', 'Miller', 'robert.miller@example.com'),
            ('Jennifer', 'Taylor', 'jennifer.taylor@example.com'),
            ('William', 'Anderson', 'william.anderson@example.com'),
            ('Elizabeth', 'Thomas', 'elizabeth.thomas@example.com'),
            ('James', 'Jackson', 'james.jackson@example.com'),
            ('Patricia', 'White', 'patricia.white@example.com'),
            ('Richard', 'Harris', 'richard.harris@example.com'),
            ('Linda', 'Martin', 'linda.martin@example.com'),
            ('Charles', 'Thompson', 'charles.thompson@example.com'),
            ('Barbara', 'Moore', 'barbara.moore@example.com'),
            ('Joseph', 'Lee', 'joseph.lee@example.com'),
            ('Susan', 'Walker', 'susan.walker@example.com'),
            ('Thomas', 'Hall', 'thomas.hall@example.com'),
            ('Jessica', 'Allen', 'jessica.allen@example.com'),
        ]
        
        for first, last, email in authors_data:
            Author.objects.get_or_create(
                first_name=first,
                last_name=last,
                defaults={'email': email}
            )
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(authors_data)} authors'))
        
        # Sample titles for different subjects
        self.stdout.write(f'Creating {count} resources...')
        
        sample_titles = {
            'Computer Science': [
                'Introduction to Machine Learning',
                'Advanced Database Systems',
                'Modern Web Development',
                'Artificial Intelligence Fundamentals',
                'Data Structures and Algorithms',
                'Software Engineering Principles',
                'Computer Networks and Security',
                'Cloud Computing Architecture',
                'Python Programming Complete Guide',
                'Cybersecurity Essentials',
            ],
            'Literature': [
                'Modern Literary Criticism',
                'Shakespeare and Contemporary Drama',
                'Poetry Through the Ages',
                'The Art of Storytelling',
                'Contemporary Fiction Analysis',
                'World Literature Survey',
                'Creative Writing Workshop',
                'American Literature History',
                'British Literary Traditions',
                'Comparative Literature Studies',
            ],
            'History': [
                'World History: A Comprehensive Study',
                'Ancient Civilizations',
                'Medieval Europe and Society',
                'Modern American History',
                'The Renaissance Period',
                'Industrial Revolution Impact',
                'World War II Chronicles',
                'Cold War and Beyond',
                'African History and Culture',
                'Asian Historical Perspectives',
            ],
            'Science': [
                'Environmental Science and Sustainability',
                'Climate Change and Global Impact',
                'Marine Biology Essentials',
                'Astronomy and Cosmology',
                'Quantum Physics Introduction',
                'Genetics and Evolution',
                'Ecology and Conservation',
                'Earth Sciences Fundamentals',
                'Space Exploration History',
                'Scientific Method and Research',
            ],
            'Medicine': [
                'Medical Diagnosis and Treatment',
                'Human Anatomy and Physiology',
                'Pharmacology Principles',
                'Public Health Strategies',
                'Clinical Medicine Practice',
                'Surgical Techniques Modern',
                'Mental Health and Wellness',
                'Epidemiology and Disease Control',
                'Medical Ethics and Law',
                'Healthcare Management Systems',
            ],
        }
        
        # Flatten all titles
        all_titles = []
        for subject_titles in sample_titles.values():
            all_titles.extend(subject_titles)
        
        # Keywords pool
        keywords_pool = [
            'research', 'analysis', 'study', 'investigation', 'methodology',
            'theory', 'practice', 'application', 'framework', 'system',
            'development', 'implementation', 'evaluation', 'assessment',
            'innovation', 'technology', 'design', 'solution', 'approach',
            'strategy', 'model', 'concept', 'principle', 'technique',
            'process', 'management', 'optimization', 'integration', 'advanced',
            'comprehensive', 'introduction', 'fundamentals', 'essentials',
        ]
        
        # Publishers
        publishers = [
            'Academic Press', 'Tech Publications', 'University Press',
            'Scientific Books', 'Global Publishers', 'Modern Education Press',
            'Knowledge House', 'Learning Publishers', 'Research Institute Press',
            'International Publishing', 'Educational Books Inc',
        ]
        
        # Locations
        locations = [
            'Main Library - First Floor',
            'Main Library - Second Floor',
            'Science Library',
            'Digital Collection',
            'Reference Section',
            'Special Collections',
            'Reserved Section',
        ]
        
        # Create resources
        created_count = 0
        for i in range(count):
            try:
                # Select random subject
                subject_list = list(Subject.objects.all())
                if not subject_list:
                    self.stdout.write(self.style.ERROR('No subjects found!'))
                    return
                
                primary_subject = random.choice(subject_list)
                
                # Create title
                base_titles = sample_titles.get(
                    primary_subject.name,
                    all_titles
                )
                title = f"{random.choice(base_titles)} - Volume {i+1}"
                
                # Generate description
                descriptions = [
                    f"Comprehensive study covering fundamental concepts and advanced topics in {primary_subject.name}.",
                    f"In-depth analysis of key principles and methodologies in {primary_subject.name}.",
                    f"Essential guide to understanding core concepts in {primary_subject.name}.",
                    f"Advanced exploration of theories and applications in {primary_subject.name}.",
                    f"Practical approach to mastering {primary_subject.name} principles.",
                ]
                description = random.choice(descriptions)
                
                abstract = f"This work presents a thorough examination of key principles in {primary_subject.name}. " \
                          f"The content is designed for both academic study and professional application, " \
                          f"providing readers with comprehensive knowledge and practical insights."
                
                # Create resource
                resource = LibraryResource.objects.create(
                    title=title,
                    description=description,
                    abstract=abstract,
                    publication_year=random.randint(2000, 2024),
                    publisher=random.choice(publishers),
                    isbn=f"978-{random.randint(1000000000, 9999999999)}",
                    call_number=f"Q{random.randint(100, 999)}.{random.randint(10, 99)} {chr(65 + i % 26)}{random.randint(10, 99)}",
                    location=random.choice(locations),
                    availability=random.choice(['available', 'available', 'digital', 'checked_out']),  # More available
                    pages=random.randint(150, 800),
                    language='English',
                    view_count=random.randint(0, 500),
                    resource_type=ResourceType.objects.order_by('?').first(),
                )
                
                # Add authors (1-3 per resource)
                authors_count = random.randint(1, 3)
                authors = Author.objects.order_by('?')[:authors_count]
                resource.authors.set(authors)
                
                # Add subjects (1-2 per resource)
                subjects_count = random.randint(1, 2)
                subjects = Subject.objects.order_by('?')[:subjects_count]
                resource.subjects.set(subjects)
                
                # Add keywords (3-7 per resource)
                keywords_count = random.randint(3, 7)
                resource_keywords = random.sample(keywords_pool, min(keywords_count, len(keywords_pool)))
                
                for keyword_text in resource_keywords:
                    keyword, created = Keyword.objects.get_or_create(
                        word=keyword_text,
                        defaults={'frequency': 1}
                    )
                    if not created:
                        keyword.frequency += 1
                        keyword.save()
                    keyword.resources.add(resource)
                
                created_count += 1
                
                # Progress indicator
                if (created_count % 10) == 0:
                    self.stdout.write(f'  Created {created_count}/{count} resources...')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating resource {i+1}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Successfully created {created_count} library resources!')
        )
        
        # Summary statistics
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('DATABASE SUMMARY:'))
        self.stdout.write('='*50)
        self.stdout.write(f'Total Resources: {LibraryResource.objects.count()}')
        self.stdout.write(f'Total Authors: {Author.objects.count()}')
        self.stdout.write(f'Total Subjects: {Subject.objects.count()}')
        self.stdout.write(f'Total Keywords: {Keyword.objects.count()}')
        self.stdout.write(f'Available Resources: {LibraryResource.objects.filter(availability="available").count()}')
        self.stdout.write(f'Digital Resources: {LibraryResource.objects.filter(availability="digital").count()}')
        self.stdout.write('='*50)
        
        self.stdout.write(
            self.style.SUCCESS('\n✓ Data population completed successfully!')
        )
        self.stdout.write(
            self.style.WARNING('\nNext steps:')
        )
        self.stdout.write('  1. Run: python manage.py runserver')
        self.stdout.write('  2. Visit: http://127.0.0.1:8000/')
        self.stdout.write('  3. Login and start exploring!')

