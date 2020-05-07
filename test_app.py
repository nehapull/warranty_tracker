import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import setup_db, Product, User, Items_for_Sale

load_dotenv()

ITEMS_PER_PAGE = 10

auth_header_for_user_token = os.environ.get('auth_header_for_user_token')

auth_header_for_user_role = {
    'Authorization': auth_header_for_user_token
}

auth_header_for_seller_token = os.environ.get('auth_header_for_seller_token')

auth_header_for_seller_role = {
    'Authorization': auth_header_for_seller_token
}


class WarrantyTestCase(unittest.TestCase):
    """This class represents the warranty test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "warranty_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for
    expected errors.
    """

    def test_post_a_product(self):
        """Test posting a new product"""

        res = self.client().post(
            '/products',
            json={
                'name': 'MacBook',
                'date_purchased': '2017-01-12',
                'warranty_end_date': '2025-01-12'
            }, headers=auth_header_for_user_role)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['products']))
        self.assertTrue(data['total_products'])

    def test_422_cannot_post_product(self):
        """Test 422 error for post request with no request data"""

        res = self.client().post('/products',
                                 headers=auth_header_for_user_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'cannot process request')

    def test_retrieve_products(self):
        """Test get request for listing out all products"""

        res = self.client().get('/products', headers=auth_header_for_user_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])
        self.assertTrue(data['total_products'])

    def test_404_cannot_retrieve_products(self):
        """Test 404 error for get request to page that does not exist"""

        res = self.client().get('/products?page=500',
                                headers=auth_header_for_user_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')

    def test_update_products(self):
        """Test update request for a product"""

        res = self.client().patch(
            '/products/2',
            headers=auth_header_for_user_role,
            json={
                'name': 'Macbook Pro'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products'])
        self.assertTrue(data['total_products'])

    def test_422_cannot_update_product(self):
        """Test 422 error for get request to page that does not exist"""

        res = self.client().patch(
            '/products/1000',
            headers=auth_header_for_user_role,
            json={
                'name': 'MacBook Air'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'cannot process request')

    """
    def test_delete_product(self):
        Test deleting a product res = self.client().delete('/products/2',
        headers=auth_header_for_user_role) data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(Product.query.filter(Product.id == 2))
        self.assertEqual(data['total_products'])
    """

    def test_404_cannot_delete_product(self):
        """Test 404 error for an invalid product ID for deleting
           product"""

        res = self.client().delete('/products/10000',
                                   headers=auth_header_for_user_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')

    def test_post_an_item(self):
        """Test posting a new item"""

        res = self.client().post(
            '/items',
            json={
                'name': 'MacBook Pro',
                'warranty_period': 2,
                'item_description': 'Brand new and good quality',
                'image_link': "getmacbookimages.com"
            }, headers=auth_header_for_seller_role)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['items']))
        self.assertTrue(data['total_items'])

    def test_422_cannot_post_item(self):
        """Test 422 error for post request with no request data"""

        res = self.client().post('/items', headers=auth_header_for_seller_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'cannot process request')

    def test_retrieve_items(self):
        """Test get request for listing out all items"""

        res = self.client().get('/items', headers=auth_header_for_seller_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['items'])
        self.assertTrue(data['total_items'])

    def test_404_cannot_retrieve_items(self):
        """Test 404 error for get request to page that does not exist"""

        res = self.client().get('/items?page=500',
                                headers=auth_header_for_seller_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')

    """
    def test_delete_item(self): Test deleting an item res =
    self.client().delete('/items/1', headers=auth_header_for_seller_role) data
    = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(Product.query.filter(Item.id == 1))
        self.assertEqual(data['total_items'])
    """

    def test_404_cannot_delete_item(self):
        """Test 404 error for an invalid item ID for deleting
           product"""

        res = self.client().delete('/items/10000',
                                   headers=auth_header_for_seller_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')

    def test_get_a_product_unauthorized(self):
        """Test retrieving a product but as a seller role"""

        res = self.client().get(
            '/products', headers=auth_header_for_seller_role)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_post_a_product_unauthorized(self):
        """Test posting a new product but as a seller role"""

        res = self.client().post(
            '/products',
            json={
                'name': 'MacBook',
                'date_purchased': '2017-01-12',
                'warranty_end_date': '2025-01-12',
            }, headers=auth_header_for_seller_role)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_update_a_product_unauthorized(self):
        """Test updating a product but as a seller role"""

        res = self.client().patch(
            '/products/1', json={
                'name': 'Macbook Pro'},
            headers=auth_header_for_seller_role)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_a_product_unauthorized(self):
        """Test deleting a product but as a seller role"""

        res = self.client().delete(
            '/products/1', headers=auth_header_for_seller_role)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_post_an_item_unauthorized(self):
        """Test posting a new item but as a user role"""

        res = self.client().post(
            '/items',
            json={
                'name': 'MacBook Pro',
                'warranty_period': 2,
                'item_description': 'Brand new and good quality',
                'image_link': "getmacbookimages.com"
            }, headers=auth_header_for_user_role)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_get_an_item_unauthorized(self):
        """Test retrieving an item but as a user role"""

        res = self.client().get('/items',
                                headers=auth_header_for_user_role)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_an_item_unauthorized(self):
        """Test deleting an item but as a user role"""

        res = self.client().delete(
            '/items/2',
            headers=auth_header_for_user_role)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
