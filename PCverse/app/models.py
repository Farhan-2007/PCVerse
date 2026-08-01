from app import db
from flask_login import UserMixin
from app import login_manager


# ================= CATEGORY =================

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship("Product", backref="category", lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"


# ================= PRODUCT =================

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    brand = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    price = db.Column(db.Float, nullable=False)

    image_file = db.Column(db.String(100), nullable=False,default="default_product.jpg")

    stock = db.Column(db.Integer, nullable=False, default=0)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.brand}')"
    

# Creating build model to store the user's build information

class Build(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(100), nullable = False)

    created_at = db.Column(db.DateTime, default = db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    items = db.relationship("BuildItem", backref = "build", lazy = True, cascade = "all, delete-orphan")

class BuildItem(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    build_id = db.Column(db.Integer, db.ForeignKey("build.id"), nullable = False)

    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable = False)

    product = db.relationship("Product", backref = "build_items", lazy = True)
# ================= USER =================

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    builds = db.relationship("Build", backref="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# ================= LOGIN =================

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))