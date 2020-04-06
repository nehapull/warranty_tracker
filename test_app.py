import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Product, User, Items_for_Sale

ITEMS_PER_PAGE = 10


auth_header_for_user_role = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9UTXlPRFUwUkRjeE9EWTBSVFZCTWpOQlJFVXdRVUUxUWtNMk9FUXdSVEV5TWtVeU1EWXhOZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1qeXF1bTE3ci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU4OTQ4YWI2NTk1MTEwYzEwY2NlNmM1IiwiYXVkIjpbIndhcnJhbnR5IiwiaHR0cHM6Ly9kZXYtanlxdW0xN3IuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NjE2MTU0OCwiZXhwIjoxNTg2MjQ3OTQ4LCJhenAiOiJqd081YXRzZHowam4zYktEcDdJcDRqMjJSaFBHN3c5cSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cHJvZHVjdHMiLCJnZXQ6cHJvZHVjdHMiLCJwYXRjaDpwcm9kdWN0cyIsInBvc3Q6cHJvZHVjdHMiXX0.lLmjri_xUJaPhBXI6UrbX4NIKpVRy6Wpb1eS_86DU89sSPzUI8NQrXeaUxZD5gIwAXocVHKAL5yMdeVoIVh02kbcPd9AYLg5YOGND2jyXKnPab5EYcCsJg0LLXi3Q2V4NXXlFp6bIQHviadPDqbZlk5u8cospeBhFMoXJY-SCG5vpqxMZkMuCe5KGs6Su6I0_WQosTFL9vq8QwmWfeRDvC_MYXnUysUFcKfXgFUMrRuFzBGfDGQkETzFVbC0k0_z1Ay1Skd_Z-AUIUwCkBo4SNTOfVMlb7PIjWJ1qsKt8eLx41zeH2ajTPpXzfpj2vf-sZJdbi9prlnRkZtd1LL9tQ'
}

auth_header_for_seller_role = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9UTXlPRFUwUkRjeE9EWTBSVFZCTWpOQlJFVXdRVUUxUWtNMk9FUXdSVEV5TWtVeU1EWXhOZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1qeXF1bTE3ci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3ZTU3Y2Q4N2VjN2IwYzgzOTcxNmVjIiwiYXVkIjpbIndhcnJhbnR5IiwiaHR0cHM6Ly9kZXYtanlxdW0xN3IuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU4NjE2NjY2MSwiZXhwIjoxNTg2MjUzMDYxLCJhenAiOiJqd081YXRzZHowam4zYktEcDdJcDRqMjJSaFBHN3c5cSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6aXRlbSIsImdldDppdGVtcyIsInBhdGNoOml0ZW0iLCJwb3N0Oml0ZW0iXX0.N5P-mwbBgqPfj23fIMmEf4g9Cc3s1B__tpGHBScvzxG8thEs9JIY0qyO-3xQWcJXDhzE0n-F5AoFl1nP62d1QVBMYVOsn6lSoLCM5D4SYHecYEqv_Ke7W7eOUIDhsmB4t_hgwz6fW1jQkjEuhd3gI04kUTYXec0MWRebGD6gwxfP8rJfSg3qWPQjqEXQZUwDAjtJ-oP_jHJCcBgmov0Besi4jaL-2VhG5ugx_b_JBYdPj28x_BotAF-mPilqkmR2IidnF3yUjV7SATe_hKvjAunn9xtyrnF2WHXi52gCpdONRO-xvsvDBViRjV2IlSwiOlzVgDKdMq06StIUl9xAhw'
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
            #self.db.session.commit()

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

        res = self.client().post('/products', headers=auth_header_for_user_role)
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

        res = self.client().get('/products?page=500', headers=auth_header_for_user_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')


    def test_update_products(self):
        """Test update request for a product"""

        res = self.client().patch('/products/2', headers=auth_header_for_user_role, json={
                                                                    'name': 'Macbook Pro'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['products']) 
        self.assertTrue(data['total_products'])

    def test_422_cannot_update_product(self):
        """Test 422 error for get request to page that does not exist"""

        res = self.client().patch('/products/1000', headers=auth_header_for_user_role, json={
                                                                      'name': 'MacBook Air'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'cannot process request')

    """ 
    def test_delete_product(self):
        Test deleting a product
        res = self.client().delete('/products/2', headers=auth_header_for_user_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(Product.query.filter(Product.id == 2))
        self.assertEqual(data['total_products'])
    """

    def test_404_cannot_delete_product(self):
        """Test 404 error for an invalid product ID for deleting
           product"""

        res = self.client().delete('/products/10000', headers=auth_header_for_user_role)
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

        res = self.client().get('/items?page=500', headers=auth_header_for_seller_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'request not found')


    """ 
    def test_delete_item(self):
        Test deleting an item
        res = self.client().delete('/items/1', headers=auth_header_for_seller_role)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(Product.query.filter(Item.id == 1))
        self.assertEqual(data['total_items'])
    """

    def test_404_cannot_delete_item(self):
        """Test 404 error for an invalid item ID for deleting
           product"""

        res = self.client().delete('/items/10000', headers=auth_header_for_seller_role)
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
            '/products/2', json={
                'name': 'Macbook Pro'},
                headers=auth_header_for_seller_role)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    def test_delete_a_product_unauthorized(self):
        """Test deleting a product but as a seller role"""

        res = self.client().delete(
            '/products/2', headers=auth_header_for_seller_role)

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

        res = self.client().get(
            '/items',
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
