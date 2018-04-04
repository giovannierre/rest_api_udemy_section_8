import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    # definisco un oggetto parser
    # e lo metto nella classe in modo che sia disponibile a tutti i metodi
    parser = reqparse.RequestParser() # definisce un oggetto parser
    # nota: il parser così definito recepisce automaticamente la request (il json payload) passata dall'utente con il metodo post o altri metodi
    
    # definisco gli argomenti del parser
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank")
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank") 
    
    # Attenzione: visto che parser appartiene alla definizione della classe e
    # non all'oggetto di classe (se no sarebbe definito come self.parser),
    # quando lo richiamo devo specificare anche la classe, quindi:
    # data = Item.parser.parse_args()
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': "User already exists."}
             
        user = UserModel(data['username'], data['password'])
        # in modo più compatto:
        # user = UserModel(**data)
        
        user.save_to_db()
            
        return {"message": "User created successfully."}, 201
        
       
    