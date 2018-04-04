from flask_restful import Resource, reqparse

from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="Field cannot be blank")
    
    def post(self, name):
        store = StoreModel(name)
        if StoreModel.find_by_name(name):
            return {'message': "A store named '{}' already exists".format(name)}
        
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred inserting the store'}
        
        return store.json()
            
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        
        return {'message': 'Store not found.'}, 404

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted.'}
            
        return {'message': 'Store not found.'}
            
class StoreList(Resource):
    def get(self):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}