import os # questo serve per Cloud9 o per Heroku
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

# dico a SQLAlchemy qual è il database a cui fare riferimento
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

# La riga seguente si mette per disattivare il tracking della
# estensione di SQLAlchemy per flask, ma rimane comunque un
# tracking di SQLAlchemy stesso che rimane "underlying",
# si fa non consumare troppe risorse
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'my_super_secret_key'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth 
# JWT crea automaticamente l'end-point '/auth'
# senza bisogno di definirlo in modo esplicito
# i metodi authenticate e identity sono definiti in security.py

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# Permette di lanciare l'applicazione su Cloud9
# NB: necessario 'import os' a inizio codice
if __name__ == '__main__':                        # in pratica dice 'se il programma è lanciato dal terminale'
    
    # collega l'applicazione di Flask all'oggetto db di SQLAlchemy
    from db import db
    db.init_app(app)
    
    # recupera alcuni riferimenti per Cloud9 e lancia l'applicazione
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True
    app.run(host=host, port=port)