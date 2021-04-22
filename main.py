from flask import Flask, request
from flask_mongoengine import MongoEngine
from flask_restful import Api, Resource, abort, fields, marshal_with
from mongoengine import EmbeddedDocument, StringField, EmbeddedDocumentField, IntField, ReferenceField

app = Flask(__name__)
api = Api(app)
app.config["MONGODB_SETTINGS"] = {
    'db': 'myRetaildb',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

product_description = {
    "_id": fields.Integer,
    "product_description": fields.String
}
price_fields = {
    "value": fields.String,
    "currency_code": fields.String,
    "product_desc": fields.Nested(product_description)
}
resource_fields = {
    "_id": fields.Integer,
    "current_price": fields.Nested(price_fields)
}


class ProductDescription(db.Document):
    _id = IntField(primary_key=True)
    product_description = StringField(required=False)


class CurrentPrice(EmbeddedDocument):
    value = StringField()
    currency_code = StringField()
    product_desc = ReferenceField(ProductDescription, required=False)


class MyRetailModel(db.Document):
    _id = IntField(primary_key=True)
    current_price = EmbeddedDocumentField(CurrentPrice)


class MyRetailApi(Resource):

    @marshal_with(resource_fields)
    def get(self, product_id):
        product = MyRetailModel.objects.get(_id=product_id)
        if not product:
            abort(404, message=f"No product with id {product_id}")
        product_desc = ProductDescription.objects.get(_id=product_id)
        product.current_price.product_desc = product_desc
        return product, 200

    @marshal_with(resource_fields)
    def post(self, product_id):
        data = request.get_json(force=True)
        product = MyRetailModel(_id=product_id,
                                current_price=data['current_price'],
                                ).save()
        return product, 201

    @marshal_with(resource_fields)
    def patch(self, product_id):
        data = request.get_json(force=True)
        if "current_price" in data:
            if "value" in data["current_price"]:
                MyRetailModel.objects(_id=product_id).update(set__current_price__value=data["current_price"]["value"])

            if "currency_code" in data["current_price"]:
                MyRetailModel.objects(_id=product_id).update(set__current_price__currency_code=data["current_price"]["currency_code"])

        return MyRetailModel.objects.get(_id=product_id), 204

    @marshal_with(resource_fields)
    def delete(self, product_id):
        if not MyRetailModel.objects.get(_id=product_id):
            abort(404, message=f"No product with id {product_id}")
        MyRetailModel.objects.get(_id=product_id).delete()
        return {}, 204


api.add_resource(MyRetailApi, '/products/<int:product_id>')

if __name__ == '__main__':
    app.run(debug=True)