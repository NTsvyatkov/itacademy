from models import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)

    dimension_id = db.Column(db.Integer, db.ForeignKey('dimensions.id'))
    dimension = db.relationship('Dimension', backref=db.backref('products', lazy='dynamic'))

    def __init__(self, name, description, price, dimension):
        self.name = name
        self.description = description
        self.price = price
        self.dimension = dimension

    def __str__(self):
        return '%s, %s, %s, %s' % (self.name, self.description, self.price, self.dimension)

    @staticmethod
    def add_product(name, description, price, dimension):
        p = Product(name, description, price, Dimension.query.filter_by(name=dimension).first())
        db.session.add(p)
        db.session.commit()

    @staticmethod
    def search_product(name):
        return Product.query.filter_by(name=name).all()

    @staticmethod
    def get(id):
        return Product.query.get(id)

    @staticmethod
    def update_product(id, new_name, new_description, new_price, new_dimension):
        entry = Product.get(id)
        entry.name = new_name
        entry.description = new_description
        entry.price = new_price
        entry.dimension = Dimension.query.filter_by(name=new_dimension).first()
        db.session.commit() 


class Dimension(db.Model):
    __tablename__ = 'dimensions'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))
    
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @staticmethod
    def get(id):
        return Dimension.query.get(id)

    @staticmethod
    def add_dimension(name):
        d = Dimension(name)
        db.session.add(d)
        db.session.commit()

    @staticmethod
    def update_dimension(id, new_name,):
        entry = Dimension.get(id)
        entry.name = new_name
        db.session.commit()