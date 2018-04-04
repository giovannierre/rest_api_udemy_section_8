from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    # definisco un oggetto parser
    # e lo metto nella classe in modo che sia disponibile a tutti i metodi
    parser = reqparse.RequestParser() # definisce un oggetto parser
    # nota: il parser così definito recepisce automaticamente la request (il json payload) passata dall'utente con il metodo post o altri metodi
    
    # definisco gli argomenti del parser
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank")
        
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item need a store id")
    
    # Attenzione: visto che parser appartiene alla definizione della classe e
    # non all'oggetto di classe (se no sarebbe definito come self.parser),
    # quando lo richiamo devo specificare anche la classe, quindi:
    # data = Item.parser.parse_args()

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "Item not found"}, 404
        
    def post(self, name):
        # se l'item esiste già, lancio un messaggio di errore.
        if ItemModel.find_by_name(name):
            return {"message": "Item '{}' already exists.".format(name)}
        
        # altrimenti creo il nuovo item
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500
        
        return item.json(), 201
        
    def delete(self, name):
        item = ItemModel.find_by_name(name)
            
        if not item:    
            return {'message': "Item doesn't exist"}
        
        try:
            item.delete_from_db()
        except:
            return {'message': 'An error occurred deleting the item'}, 500
        
        return {'message': 'Item deleted successfully.'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if not item:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        
        item.save_to_db()
        
        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # Una alternativa, ma per me meno leggibile, sarebbe questa
        # (concetto di map/reduce):
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}