import unittest

import requests

BASE_URL = "http://127.0.0.1:5000/"
USER_CREDENTIALS = {"username": "Pooja", "password": "@123"}


def get_jwt_token():
    response = requests.post(BASE_URL + "/auth", json={"username": "Pooja", "password": "@123"})
    return response.json()['access_token']


class MyRetailAPITest(unittest.TestCase):

    def test_home_route(self):
        response = requests.get(BASE_URL + "/")
        self.assertEqual(response.text, '<h1>MyRetail API</h1>')
        self.assertEqual(response.status_code, 200)

    def test_get_all_products(self):
        response = requests.get(BASE_URL + "/products/")
        self.assertEqual(response.status_code, 200)

    def test_get_product_by_id(self):
        response = requests.get(BASE_URL + "/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'_id': 1,
                                           'current_price': {'currency_code': 'INR',
                                                             'product_desc': {
                                                                              'product_description': 'Washing Machine'},
                                                             'value': '45000'}})

    def test_post_without_auth(self):
        response = requests.post(BASE_URL + "/products/100")
        self.assertEqual(response.status_code, 401)

    def test_jwt_token(self):
        response = requests.post(BASE_URL + "/auth", json=USER_CREDENTIALS)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = requests.post(BASE_URL + "/products/200", headers={'Authorization': f'JWT {get_jwt_token()}'},
                                 json={
                                     'current_price': {'currency_code': 'INR',
                                                       'value': '45000'}
                                 }
                                 )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'_id': 200, 'current_price': {'value': '45000', 'currency_code': 'INR',
                                                                         'product_desc': {
                                                                             'product_description': None}}})

    def test_delete(self):
        requests.post(BASE_URL + "/products/200", headers={'Authorization': f'JWT {get_jwt_token()}'},
                      json={
                          'current_price': {'currency_code': 'INR',
                                            'value': '45000'}
                      }
                      )
        response = requests.delete(BASE_URL + "/products/200", headers={'Authorization': f'JWT {get_jwt_token()}'})
        self.assertEqual(response.status_code, 204)

    def test_patch(self):
        requests.post(BASE_URL + "/products/200", headers={'Authorization': f'JWT {get_jwt_token()}'},
                      json={
                          'current_price': {'currency_code': 'INR',
                                            'value': '45000'}
                      }
                      )
        response = requests.patch(BASE_URL + "/products/200", headers={'Authorization': f'JWT {get_jwt_token()}'},
                                  json={
                                      'current_price': {'currency_code': 'USD',
                                                        'value': '130.55'}
                                  }
                                  )

        self.assertEqual(response.status_code, 204)
