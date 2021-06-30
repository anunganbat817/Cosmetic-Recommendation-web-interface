from app import db 

class SkinCare(db.Model):
    __tablename__ = "SkinCare"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    brand = db.Column(db.String)
    category = db.Column(db.String)
    price = db.Column(db.Float)
    no_reviews = db.Column(db.Integer)
    size1 = db.Column(db.Float)
    url = db.Column(db.String)
    ingredients = db.Column(db.String) 
    list_of_ingredients = db.Column(db.String)
    price_per_ml = db.Column(db.Float)

    def __repr__(self):
        return "{}".format(self.name)

