from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    # SQLAlchemy con il metodo relatioship crea un join tra
    # le tabelle e rende disponibile un campo items.store da 
    # cui si possono avere tutte le informazioni collegate (es. items.store.name)
    
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    def json(self):
        return {'name': self.name, 'price': self.price}
        
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        
    def save_to_db(self):
        # funziona sia per insert che per update;
        # se l'id dell'oggetto passato esiste già nel db, allora
        # fa l'udpate, altrimenti fa l'insert
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()