from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True, nullable = False)

    products = db.relationship('Product', backref = 'category', lazy = True)

    def __ref__(self):
        return f"Catefory('{self.name}')"
    
class Product(db.Model):

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(100), nullable = False)

    author = db.Column(db.String(100), nullable = False)
    
    description = db.Column(db.Text, nullable = False)

    price = db.Column(db.Float, nullable = False)

    image_file = db.Column(
        db.String(100),
        nullable=False,
        default='default_product.jpg'
    )

    stock = db.Column(db.Integer, default = 0)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=False
    )    
    
    def __repr__(self):
        return f"Product('{self.name}', '{self.author}')"
