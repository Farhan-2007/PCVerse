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
                name="Python Crash Course",
                author = "Eric Matthes",
                description="Learn Python from scratch",
                price=699,
                stock=20,
                category_id=programming.id
            ),

            Product(
                name="Clean Code",
                author = "Robert C.Martin",
                description="Best practices for programmers",
                price=899,
                stock=15,
                category_id=programming.id
            ),

            Product(
                name="Atomic Habits",
                author = "James Clear",
                description="Build better habits",
                price=499,
                stock=25,
                category_id=self_help.id
            ),

            Product(
                name="The Alchemist",
                author = "Paulo Coelho",
                description="Popular fiction novel",
                price=299,
                stock=30,
                category_id=fiction.id
            )
        ]

        db.session.add_all(books)
        db.session.commit()

        print("Sample data inserted!")

    else:
        print("Database already contains data.")