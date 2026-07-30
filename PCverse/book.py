from app import create_app, db
from app.models import Category, Product

app = create_app()

with app.app_context():

    if Category.query.count() == 0:

        programming = Category(name="Programming")
        fiction = Category(name="Fiction")
        self_help = Category(name="Self Help")

        db.session.add_all([
            programming,
            fiction,
            self_help
        ])

        db.session.commit()

        books = [
            Product(
                name="To Kill a Mockingbird",
                author = "Harper Lee",
                description="A powerful story exploring justice, morality, and racial inequality in the American South",
                price=699,
                stock=20,
                image_file = "mocking_bird.jpg",
                category_id=fiction.id
            ),

            Product(
                name="The Silent Patient",
                author = "Alex Michaelides",
                description=" by Alex Michaelides: A gripping psychological thriller about a famous painter who shoots her husband and never speaks another word.",
                price=899,
                stock=15,
                image_file = "silent.jpeg",
                category_id= fiction.id
            ),

            Product(
                name="Atomic Habits",
                author = "James Clear",
                description="Build better habits",
                price=499,
                stock=25,
                image_file = "atomic.jpg",
                category_id=self_help.id
            ),

            Product(
                name="The Alchemist",
                author = "Paulo Coelho",
                description="Popular fiction novel",
                price=299,
                stock=30,
                image_file = "alchemist.jpg",
                category_id=fiction.id
            )
        ]

        db.session.add_all(books)
        db.session.commit()

        print("Sample data inserted!")

    else:
        print("Database already contains data.")