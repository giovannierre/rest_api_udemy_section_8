from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    # sulla base della foreign key definita in ItemModel è possibile
    # stabilire una relazione fra StoreModel e ItemModel
    items = db.relationship('ItemModel', lazy='dynamic')
    # NB: il parametro lazy='dynamic' è fondamentale per fare in modo
    # che l'oggetto items venga creato solo quando è lanciata una query
    # che lo interessa e così risparmiare risorse. D'altra parte
    # la contropartita è che il join deve essere ricreato ad ogni richiesta
    # e quindi l'accesso risulta più lento. La scelta è una questione di
    # compromesso e va valutato di caso in caso.
    
    def __init__(self, name):
        self.name = name
   
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
        
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