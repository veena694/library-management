from library.models import Category, Author, Book, Review
from django.contrib.auth.models import User

print("🚀 Starting library population...")

# Create superuser if doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@library.com', 'admin123')
    print("✅ Admin user created (username: admin, password: admin123)")

# Create Categories with icons
categories_data = [
    {'name': 'Science Fiction', 'icon': '🚀', 'description': 'Futuristic stories, space exploration, and advanced technology'},
    {'name': 'Mystery & Thriller', 'icon': '🔍', 'description': 'Detective stories, crime fiction, and suspenseful tales'},
    {'name': 'Romance', 'icon': '💕', 'description': 'Love stories, relationships, and emotional journeys'},
    {'name': 'Technology & Programming', 'icon': '💻', 'description': 'Computer science, software development, and tech guides'},
    {'name': 'History & Biography', 'icon': '📜', 'description': 'Historical events, personal stories, and cultural evolution'},
    {'name': 'Self-Help & Personal Development', 'icon': '🌟', 'description': 'Growth, motivation, and life improvement strategies'},
    {'name': 'Fantasy', 'icon': '🐉', 'description': 'Magical worlds, mythical creatures, and epic adventures'},
    {'name': 'Business & Economics', 'icon': '💼', 'description': 'Entrepreneurship, finance, and business strategy'},
    {'name': 'Science & Nature', 'icon': '🔬', 'description': 'Scientific discoveries, natural phenomena, and research'},
    {'name': 'Philosophy & Psychology', 'icon': '🧠', 'description': 'Mindfulness, human behavior, and philosophical thought'},
]

print("\n📚 Creating categories...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"  ✅ {cat_data['icon']} {cat_data['name']}")

# Create Authors
authors_data = [
    {'name': 'Isaac Asimov', 'biography': 'Prolific science fiction author and biochemistry professor, known for the Foundation series and Three Laws of Robotics.'},
    {'name': 'Agatha Christie', 'biography': 'Best-selling novelist of all time, creator of Hercule Poirot and Miss Marple.'},
    {'name': 'Jane Austen', 'biography': 'English novelist known for her romance novels and sharp social commentary.'},
    {'name': 'Robert C. Martin', 'biography': 'Software engineer and author, known as "Uncle Bob", advocate of agile software development.'},
    {'name': 'Yuval Noah Harari', 'biography': 'Israeli historian and philosopher, author of Sapiens and Homo Deus.'},
    {'name': 'Dale Carnegie', 'biography': 'American writer and lecturer, pioneer in self-improvement and interpersonal skills.'},
    {'name': 'J.K. Rowling', 'biography': 'British author, creator of the Harry Potter fantasy series.'},
    {'name': 'George Orwell', 'biography': 'English novelist and essayist, known for 1984 and Animal Farm.'},
    {'name': 'Stephen King', 'biography': 'Prolific horror and suspense author, master of contemporary fiction.'},
    {'name': 'Malcolm Gladwell', 'biography': 'Canadian journalist and author, known for unique perspectives on social phenomena.'},
    {'name': 'James Clear', 'biography': 'Writer and speaker focused on habits, decision making, and continuous improvement.'},
    {'name': 'Daniel Kahneman', 'biography': 'Nobel Prize winner in Economics, pioneer in behavioral economics and psychology.'},
    {'name': 'Ray Dalio', 'biography': 'Founder of Bridgewater Associates, billionaire investor and philanthropist.'},
    {'name': 'J.R.R. Tolkien', 'biography': 'English writer and philologist, creator of Middle-earth and The Lord of the Rings.'},
    {'name': 'Dan Brown', 'biography': 'American author known for thriller novels including The Da Vinci Code.'},
]

print("\n✍️ Creating authors...")
for author_data in authors_data:
    author, created = Author.objects.get_or_create(
        name=author_data['name'],
        defaults=author_data
    )
    if created:
        print(f"  ✅ {author_data['name']}")

# Get categories
sci_fi = Category.objects.get(name='Science Fiction')
mystery = Category.objects.get(name='Mystery & Thriller')
romance = Category.objects.get(name='Romance')
tech = Category.objects.get(name='Technology & Programming')
history = Category.objects.get(name='History & Biography')
self_help = Category.objects.get(name='Self-Help & Personal Development')
fantasy = Category.objects.get(name='Fantasy')
business = Category.objects.get(name='Business & Economics')
science = Category.objects.get(name='Science & Nature')
philosophy = Category.objects.get(name='Philosophy & Psychology')

# Create comprehensive book collection
books_data = [
    {
        'title': 'Foundation',
        'authors': ['Isaac Asimov'],
        'category': sci_fi,
        'isbn': '9780553293357',
        'publisher': 'Spectra',
        'publication_year': 1951,
        'description': 'For twelve thousand years the Galactic Empire has ruled supreme. Now it is dying. But only Hari Seldon, creator of the revolutionary science of psychohistory, can see into the future—to a dark age of ignorance, barbarism, and warfare that will last thirty thousand years. To preserve knowledge and save humankind, Seldon gathers the best minds in the Empire—both scientists and scholars—and brings them to a bleak planet at the edge of the galaxy to serve as a beacon of hope for future generations.',
        'keywords': 'science fiction, space opera, psychohistory, galactic empire, future, foundation, hari seldon, asimov',
        'pages': 255,
        'copies_total': 5,
        'copies_available': 3,
        'availability': 'available',
        'rating': 4.5,
    },
    {
        'title': 'Murder on the Orient Express',
        'authors': ['Agatha Christie'],
        'category': mystery,
        'isbn': '9780062693662',
        'publisher': 'William Morrow',
        'publication_year': 1934,
        'description': 'Just after midnight, the famous Orient Express is stopped in its tracks by a snowdrift. By morning, the millionaire Samuel Edward Ratchett lies dead in his compartment, stabbed a dozen times, his door locked from the inside. Without a shred of doubt, one of the thirteen passengers killed the odious Ratchett. The question is: which one? Detective Hercule Poirot must solve this seemingly impossible case before the killer strikes again.',
        'keywords': 'mystery, detective, murder, train, hercule poirot, crime, investigation, whodunit, christie',
        'pages': 256,
        'copies_total': 4,
        'copies_available': 4,
        'availability': 'available',
        'rating': 4.7,
    },
    {
        'title': 'Pride and Prejudice',
        'authors': ['Jane Austen'],
        'category': romance,
        'isbn': '9780141439518',
        'publisher': 'Penguin Classics',
        'publication_year': 1813,
        'description': 'When Elizabeth Bennet meets the wealthy Mr. Darcy, she finds him arrogant and conceited. When she later discovers that Darcy has involved himself in the troubled relationship between his friend Bingley and her beloved sister Jane, she is determined to dislike him more than ever. But in the sparkling comedy of manners that follows, Jane Austen shows the folly of making hasty judgments and reveals the true nature of character.',
        'keywords': 'romance, classic, elizabeth bennet, mr darcy, regency, england, love, society, austen',
        'pages': 432,
        'copies_total': 6,
        'copies_available': 5,
        'availability': 'available',
        'rating': 4.8,
    },
    {
        'title': 'Clean Code: A Handbook of Agile Software Craftsmanship',
        'authors': ['Robert C. Martin'],
        'category': tech,
        'isbn': '9780132350884',
        'publisher': 'Prentice Hall',
        'publication_year': 2008,
        'description': 'Even bad code can function. But if code isn\'t clean, it can bring a development organization to its knees. Every year, countless hours and significant resources are lost because of poorly written code. This book will teach you the best practices for writing clean, maintainable code. Through carefully selected examples and case studies, you\'ll learn how to distinguish good code from bad code and how to transform bad code into good code.',
        'keywords': 'programming, software engineering, code quality, best practices, refactoring, clean code, design patterns, agile',
        'pages': 464,
        'copies_total': 10,
        'copies_available': 7,
        'availability': 'available',
        'rating': 4.6,
    },
    {
        'title': 'Sapiens: A Brief History of Humankind',
        'authors': ['Yuval Noah Harari'],
        'category': history,
        'isbn': '9780062316110',
        'publisher': 'Harper',
        'publication_year': 2014,
        'description': 'From a renowned historian comes a groundbreaking narrative of humanity\'s creation and evolution that explores the ways in which biology and history have defined us and enhanced our understanding of what it means to be human. 100,000 years ago, at least six different species of humans inhabited Earth. Yet today there is only one—homo sapiens. What happened to the others? And what may happen to us?',
        'keywords': 'history, anthropology, evolution, human civilization, prehistory, sapiens, harari, humanity',
        'pages': 443,
        'copies_total': 8,
        'copies_available': 6,
        'availability': 'available',
        'rating': 4.7,
    },
    {
        'title': 'How to Win Friends and Influence People',
        'authors': ['Dale Carnegie'],
        'category': self_help,
        'isbn': '9780671027032',
        'publisher': 'Pocket Books',
        'publication_year': 1936,
        'description': 'You can go after the job you want—and get it! You can take the job you have—and improve it! You can take any situation—and make it work for you! Dale Carnegie\'s rock-solid, time-tested advice has carried countless people up the ladder of success in their business and personal lives. His principles endure and will help you achieve your maximum potential.',
        'keywords': 'self-help, communication, relationships, influence, leadership, personal development, social skills, carnegie',
        'pages': 288,
        'copies_total': 7,
        'copies_available': 7,
        'availability': 'available',
        'rating': 4.5,
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'authors': ['J.K. Rowling'],
        'category': fantasy,
        'isbn': '9780439708180',
        'publisher': 'Scholastic',
        'publication_year': 1997,
        'description': 'Harry Potter has never even heard of Hogwarts when the letters start dropping on the doormat at number four, Privet Drive. Addressed in green ink on yellowish parchment with a purple seal, they are swiftly confiscated by his grisly aunt and uncle. Then, on Harry\'s eleventh birthday, a great beetle-eyed giant of a man called Rubeus Hagrid bursts in with some astonishing news: Harry Potter is a wizard.',
        'keywords': 'fantasy, magic, wizard, hogwarts, harry potter, young adult, adventure, magical, rowling',
        'pages': 309,
        'copies_total': 12,
        'copies_available': 8,
        'availability': 'available',
        'rating': 4.9,
    },
    {
        'title': '1984',
        'authors': ['George Orwell'],
        'category': sci_fi,
        'isbn': '9780451524935',
        'publisher': 'Signet Classic',
        'publication_year': 1949,
        'description': 'Among the seminal texts of the 20th century, Nineteen Eighty-Four is a rare work that grows more haunting as its futuristic purgatory becomes more real. Published in 1949, the book offers political satirist George Orwell\'s nightmare vision of a totalitarian, bureaucratic world and one poor stiff\'s attempt to find individuality. The brilliance of the novel is Orwell\'s prescience of modern life.',
        'keywords': 'dystopia, totalitarianism, surveillance, big brother, thought police, orwell, political, classic',
        'pages': 328,
        'copies_total': 6,
        'copies_available': 4,
        'availability': 'available',
        'rating': 4.8,
    },
    {
        'title': 'The Shining',
        'authors': ['Stephen King'],
        'category': mystery,
        'isbn': '9780307743657',
        'publisher': 'Anchor',
        'publication_year': 1977,
        'description': 'Jack Torrance\'s new job at the Overlook Hotel is the perfect chance for a fresh start. As the off-season caretaker at the atmospheric old hotel, he\'ll have plenty of time to spend reconnecting with his family and working on his writing. But as the harsh winter weather sets in, the idyllic location feels ever more remote and more sinister. And the only one to notice the strange and terrible forces gathering around the Overlook is Danny Torrance, a uniquely gifted five-year-old.',
        'keywords': 'horror, thriller, supernatural, haunted hotel, isolation, king, psychological, suspense',
        'pages': 659,
        'copies_total': 5,
        'copies_available': 3,
        'availability': 'available',
        'rating': 4.6,
    },
    {
        'title': 'Atomic Habits',
        'authors': ['James Clear'],
        'category': self_help,
        'isbn': '9780735211292',
        'publisher': 'Avery',
        'publication_year': 2018,
        'description': 'No matter your goals, Atomic Habits offers a proven framework for improving every day. James Clear, one of the world\'s leading experts on habit formation, reveals practical strategies that will teach you exactly how to form good habits, break bad ones, and master the tiny behaviors that lead to remarkable results. If you\'re having trouble changing your habits, the problem isn\'t you. The problem is your system.',
        'keywords': 'habits, self-improvement, productivity, behavior change, personal growth, systems, routine, clear',
        'pages': 320,
        'copies_total': 15,
        'copies_available': 10,
        'availability': 'available',
        'rating': 4.8,
    },
    {
        'title': 'Thinking, Fast and Slow',
        'authors': ['Daniel Kahneman'],
        'category': philosophy,
        'isbn': '9780374533557',
        'publisher': 'Farrar, Straus and Giroux',
        'publication_year': 2011,
        'description': 'In this work, Daniel Kahneman, the renowned psychologist and winner of the Nobel Prize in Economics, takes us on a groundbreaking tour of the mind and explains the two systems that drive the way we think. System 1 is fast, intuitive, and emotional; System 2 is slower, more deliberative, and more logical. The impact of overconfidence on corporate strategies, the difficulties of predicting what will make us happy in the future, the profound effect of cognitive biases.',
        'keywords': 'psychology, thinking, decision making, behavioral economics, cognitive bias, kahneman, nobel, mind',
        'pages': 499,
        'copies_total': 6,
        'copies_available': 5,
        'availability': 'available',
        'rating': 4.7,
    },
    {
        'title': 'Principles: Life and Work',
        'authors': ['Ray Dalio'],
        'category': business,
        'isbn': '9781501124020',
        'publisher': 'Simon & Schuster',
        'publication_year': 2017,
        'description': 'Ray Dalio, one of the world\'s most successful investors and entrepreneurs, shares the unconventional principles that he\'s developed, refined, and used over the past forty years to create unique results in both life and business—and which any person or organization can adopt to help achieve their goals. Dalio believes that everything happens over and over again, and that by studying these patterns, we can better understand how reality works.',
        'keywords': 'business, investment, principles, success, management, decision making, dalio, leadership, finance',
        'pages': 592,
        'copies_total': 8,
        'copies_available': 7,
        'availability': 'available',
        'rating': 4.6,
    },
    {
        'title': 'The Lord of the Rings: The Fellowship of the Ring',
        'authors': ['J.R.R. Tolkien'],
        'category': fantasy,
        'isbn': '9780544003415',
        'publisher': 'Mariner Books',
        'publication_year': 1954,
        'description': 'In ancient times the Rings of Power were crafted by the Elven-smiths, and Sauron, the Dark Lord, forged the One Ring, filling it with his own power so that he could rule all others. But the One Ring was taken from him, and though he sought it throughout Middle-earth, it remained lost to him. After many ages it fell into the hands of Bilbo Baggins, as told in The Hobbit. In a sleepy village in the Shire, young Frodo Baggins finds himself faced with an immense task.',
        'keywords': 'fantasy, epic, middle earth, adventure, hobbits, ring, tolkien, quest, magic, elves',
        'pages': 423,
        'copies_total': 7,
        'copies_available': 5,
        'availability': 'available',
        'rating': 4.9,
    },
    {
        'title': 'The Da Vinci Code',
        'authors': ['Dan Brown'],
        'category': mystery,
        'isbn': '9780307474278',
        'publisher': 'Anchor',
        'publication_year': 2003,
        'description': 'While in Paris, Harvard symbologist Robert Langdon is awakened by a phone call in the dead of the night. The elderly curator of the Louvre has been murdered inside the museum, his body covered in baffling symbols. As Langdon and gifted French cryptologist Sophie Neveu sort through the bizarre riddles, they are stunned to discover a trail of clues hidden in the works of Leonardo da Vinci—clues visible for all to see and yet ingeniously disguised by the painter.',
        'keywords': 'thriller, mystery, codes, symbols, religious, conspiracy, art, langdon, brown, suspense',
        'pages': 489,
        'copies_total': 8,
        'copies_available': 6,
        'availability': 'available',
        'rating': 4.4,
    },
    {
        'title': 'A Brief History of Time',
        'authors': ['Stephen King'],
        'category': science,
        'isbn': '9780553380163',
        'publisher': 'Bantam',
        'publication_year': 1988,
        'description': 'Stephen Hawking, one of the most brilliant theoretical physicists in history, wrote the modern classic A Brief History of Time to help nonscientists understand fundamental questions of physics and our existence: Where did the universe come from? How and why did it begin? Will it come to an end, and if so, how? Hawking attempts to reveal these questions (and where we\'re looking for answers) using a minimum of technical jargon.',
        'keywords': 'science, physics, cosmology, universe, black holes, time, hawking, space, astronomy, theory',
        'pages': 256,
        'copies_total': 5,
        'copies_available': 4,
        'availability': 'available',
        'rating': 4.5,
    },
]

print("\n📖 Creating books...")
for book_data in books_data:
    author_names = book_data.pop('authors')
    
    book, created = Book.objects.get_or_create(
        isbn=book_data['isbn'],
        defaults=book_data
    )
    
    if created:
        # Add authors
        for author_name in author_names:
            author = Author.objects.get(name=author_name)
            book.authors.add(author)
        
        print(f"  ✅ {book.title}")

# Add some reviews
print("\n⭐ Creating sample reviews...")
admin_user = User.objects.get(username='admin')
sample_books = Book.objects.all()[:5]

reviews_data = [
    {'rating': 5, 'comment': 'An absolute masterpiece! Highly recommend to everyone.'},
    {'rating': 4, 'comment': 'Great read, though a bit slow at times. Overall very enjoyable.'},
    {'rating': 5, 'comment': 'Changed my perspective completely. A must-read!'},
    {'rating': 4, 'comment': 'Well-written and engaging. Looking forward to reading more from this author.'},
    {'rating': 5, 'comment': 'Could not put it down! Brilliant from start to finish.'},
]

for book, review_data in zip(sample_books, reviews_data):
    Review.objects.get_or_create(
        book=book,
        user=admin_user,
        defaults=review_data
    )
    print(f"  ✅ Review for {book.title}")

print("\n" + "="*50)
print("🎉 Library population completed successfully!")
print("="*50)
print(f"\n📊 Summary:")
print(f"  • Categories: {Category.objects.count()}")
print(f"  • Authors: {Author.objects.count()}")
print(f"  • Books: {Book.objects.count()}")
print(f"  • Reviews: {Review.objects.count()}")
print(f"\n👤 Admin credentials:")
print(f"  Username: admin")
print(f"  Password: admin123")
print(f"\n🌐 Access the system at: http://127.0.0.1:8000/")
print(f"🔐 Admin panel at: http://127.0.0.1:8000/admin/")
print("\n✨ Happy reading! ✨\n")