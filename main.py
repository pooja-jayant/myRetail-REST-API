from flask import Flask, request, make_response
from flask_mongoengine import MongoEngine
from flask_restful import Api, Resource, abort, fields, marshal_with
from mongoengine import EmbeddedDocument, StringField, EmbeddedDocumentField, IntField, ReferenceField
from flask_jwt import JWT, jwt_required, JWTError
from security.security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = 'secret'
jwt = JWT(app, authenticate, identity)
app.config["MONGODB_SETTINGS"] = {
    'db': 'myRetaildb',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

product_description = {
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

multiple_products = {
    "products": fields.List(fields.Nested(resource_fields))
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
        try:
            product = MyRetailModel.objects.get(_id=product_id)
            if not product:
                abort(404, message=f"No product with id {product_id}")
            result = ProductDescription.objects.with_id(object_id=product_id)
            if result:
                product_desc = ProductDescription.objects.get(_id=product_id)
                product.current_price.product_desc = product_desc
            return product, 200
        except Exception:
            return {}, 404

    @marshal_with(resource_fields)
    @jwt_required()
    def post(self, product_id):
        try:
            data = request.get_json(force=True)
            product = MyRetailModel(_id=product_id,
                                    current_price=data['current_price'],
                                    ).save()
            result = ProductDescription.objects.with_id(object_id=product_id)
            if result:
                product_desc = ProductDescription.objects.get(_id=product_id)
                if product_desc:
                    product.current_price.product_desc = product_desc
            return product, 201
        except JWTError:
            return {}, 422

    @marshal_with(resource_fields)
    @jwt_required()
    def patch(self, product_id):
        try:
            data = request.get_json(force=True)
            if "current_price" in data:
                if "value" in data["current_price"]:
                    MyRetailModel.objects.get(_id=product_id).update(
                        set__current_price__value=data["current_price"]["value"])

                if "currency_code" in data["current_price"]:
                    MyRetailModel.objects.get(_id=product_id).update(
                        set__current_price__currency_code=data["current_price"]["currency_code"])
            product = MyRetailModel.objects.get(_id=product_id)
            result = ProductDescription.objects.with_id(object_id=product_id)
            if result:
                product_desc = ProductDescription.objects.get(_id=product_id)
                if product_desc:
                    product.current_price.product_desc = product_desc
            return product, 204
        except JWTError as jwt_error:
            return {"error": jwt_error}, 401
        except Exception:
            return {"error": "Failed to Update!!"}, 500

    @jwt_required()
    def delete(self, product_id):
        try:
            if not MyRetailModel.objects.with_id(object_id=product_id):
                return {"error": f"product with id {product_id} does not exist"}, 404
            MyRetailModel.objects.get(_id=product_id).delete()
            return {"msg": "deleted!!"}, 204

        except JWTError as jwt_error:
            return {"error": jwt_error}, 401

        except Exception as e:
            return {"error": e}, 500


class GetAllProducts(Resource):

    @marshal_with(multiple_products)
    def get(self):
        try:
            products = MyRetailModel.objects.filter()
            updated_products = []
            for product in products:
                result = ProductDescription.objects.with_id(object_id=product._id)
                if result:
                    product_desc = ProductDescription.objects.get(_id=product._id)
                    product.current_price.product_desc = product_desc
                    updated_products.append(product)
                else:
                    updated_products.append(product)
            return {"products": updated_products}, 200
        except Exception:
            return {}, 404


class Home(Resource):

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response("<h1>MyRetail API</h1>", headers)


api.add_resource(Home, '/')
api.add_resource(GetAllProducts, '/products/')
api.add_resource(MyRetailApi, '/products/<int:product_id>')


if __name__ == '__main__':
    app.run(debug=True)
