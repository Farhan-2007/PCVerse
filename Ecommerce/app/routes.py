from flask import Blueprint, render_template
from app.models import Product, Category

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("home.html")


@main.route("/books")
def books():
    books = Product.query.order_by(Product.name.asc()).all()
    categories = Category.query.all()

    return render_template(
        "books.html",
        books=books,
        categories=categories
    )


@main.route("/book/<int:book_id>")
def book(book_id):
    book = Product.query.get_or_404(book_id)

    return render_template("book.html", book=book)


@main.route("/category/<int:category_id>")
def category_books(category_id):
    category = Category.query.get_or_404(category_id)

    books = Product.query.filter_by(category_id=category_id).all()

    return render_template(
        "category.html",
        category=category,
        books=books
    )