from flask import Blueprint, render_template
from app.models import Product

main = Blueprint('main', __name__)

@main.route("/")
def home():
    books = Product.query.order_by(Product.name.asc()).all()
    return render_template("home.html", books = books)

@main.route("/book/<int:book_id>")
def book(book_id):
    book = Product.query.get_or_404(book_id)

    return render_template("book.html", book = book)
