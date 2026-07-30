from app import db
from flask_login import UserMixin
from app import login_manager


class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100),unique=True,nullable=False)

    products = db.relationship('Product',backref='category',lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"


class Product(db.Model):

    id = db.Column( db.Integer,primary_key=True)

    name = db.Column(db.String(100),nullable=False)

    brand = db.Column(db.String(100),nullable=False)

    description = db.Column(db.Text,nullable=False)

    price = db.Column(db.Float,nullable=False)

    image_file = db.Column(db.String(100),nullable=False,default='default_product.jpg')

    stock = db.Column(db.Integer,default=0)

    category_id = db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.brand}')"


class User(UserMixin, db.Model):

    id = db.Column(db.Integer,primary_key=True)

    username = db.Column(db.String(20),unique=True,nullable=False)

    email = db.Column(db.String(120),unique=True,nullable=False)

    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))