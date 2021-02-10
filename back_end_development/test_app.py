import unittest
import json
from flask import Flask
from app import app

class BoshMallTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.from_object('config')
        self.client = self.app.test_client
    
    def test_initial_route_pass(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], 'BoshMall API')
        self.assertTrue(data['success'])

    '''
    Product Tests
    #########################################################
    '''
    def test_get_products_route_pass(self):
        res = self.client().get('/products')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['products']), 0)
        self.assertGreater(data['total_products'], 0)
        self.assertGreater(len(data['cats']), 0)
        self.assertGreater(len(data['tags']), 0)
    
    def test_get_products_route_page_out_of_range(self):
        res = self.client().get('/products?page=982374923')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['products']), 0)
    
    def test_get_product_route_with_valid_id(self):
        res = self.client().get('/products/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data), 0)
        self.assertIsNotNone(data)

    def test_get_product_route_with_invalid_id(self):
        res = self.client().get('/products/9823647926734')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], 'resource was not found')

    def test_add_product_route_pass(self):
        res = self.client().post('/products', json={ 'name': "testUser",  'description': 'test description', 'price': 11, 'image_url': '', 'seller_id':1,  'cat_id': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(data['product_id'], 0)

    def test_add_product_route_fail(self):
        res = self.client().post('/products', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

    def test_update_product_route_pass(self):
        res = self.client().patch('/products/11', json={ 'name': "testProduct"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['product']), 0)

    def test_update_product_route_fail(self):
        res = self.client().patch('/products/98723649', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])
    
    def test_delete_product_route_pass(self):
        product = self.client().post('/products', json={ 'name': "testUser",  'description': 'test description', 'price': 11, 'image_url': '', 'seller_id':1,  'cat_id': 1})
        product = json.loads(product.data)
        res = self.client().delete('/products/' + str(product['product_id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['product']['id'], product['product_id'])

    def test_delete_product_route_fail(self):
        res = self.client().delete('/products/98723649')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

    def test_sell_product_route_pass(self):
        original_poduct_response =  self.client().get('/products/11')
        original_data = json.loads(original_poduct_response.data)
        res = self.client().patch('/sell_product/11')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data), 0)
        self.assertNotEqual(original_data['num_of_sales'], data['num_of_sales'])
        self.assertNotEqual(original_data['total_sales'], data['total_sales'])

    def test_sell_product_route_fail(self):
        res = self.client().patch('/sell_product/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource was not found')
        self.assertFalse(data['success'])

    '''
    Seller Tests
    #########################################################
    '''
    def test_get_sellers_route_pass(self):
        res = self.client().get('/sellers')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['sellers']), 0)
        self.assertGreater(data['total_sellers'], 0)
    
    def test_get_sellers_route_page_out_of_range(self):
        res = self.client().get('/sellers?page=982374923')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['sellers']), 0)
    
    def test_get_seller_route_with_valid_id(self):
        res = self.client().get('/sellers/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data), 0)
        self.assertIsNotNone(data)

    def test_get_seller_route_with_invalid_id(self):
        res = self.client().get('/sellers/9823647926734')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], 'resource was not found')

    def test_add_seller_route_pass(self):
        res = self.client().post('/sellers', json={ 'avatar': 'asdfasd f', 'facebook_link': 'asdfasdf', 'name': 'testSeller', 'phone_number': '234234', 'store_description': 'asdf asdf', 'website': 'asdfas f'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(data['seller_id'], 0)

    def test_add_seller_route_fail(self):
        res = self.client().post('/sellers', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

    def test_update_seller_route_pass(self):
        res = self.client().patch('/sellers/2', json={ 'name': "testseller"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['seller']), 0)

    def test_update_seller_route_fail(self):
        res = self.client().patch('/sellers/98723649', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])
    
    def test_delete_seller_route_pass(self):
        seller = self.client().post('/sellers', json={ 'avatar': 'asdfasd f', 'facebook_link': 'asdfasdf', 'name': 'testSeller123213', 'phone_number': '234234', 'store_description': 'asdf asdf', 'website': 'asdfas f'})
        seller = json.loads(seller.data)
        res = self.client().delete('/sellers/' + str(seller['seller_id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['seller']['id'], seller['seller_id'])

    def test_delete_seller_route_fail(self):
        res = self.client().delete('/sellers/98723649')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

    
    '''
    Category Tests
    #########################################################
    '''
    def test_get_categories_route_pass(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['categories']), 0)
        self.assertGreater(data['total_categories'], 0)
    
    def test_get_category_route_with_valid_id(self):
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data), 0)
        self.assertIsNotNone(data)

    def test_get_category_route_with_invalid_id(self):
        res = self.client().get('/categories/9823647926734')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], 'resource was not found')

    def test_add_category_route_pass(self):
        res = self.client().post('/categories', json={ 'name': 'test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(data['category_id'], 0)

    def test_add_category_route_fail(self):
        res = self.client().post('/categories', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

    def test_update_category_route_pass(self):
        res = self.client().patch('/categories/2', json={ 'name': "testcategory"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['category']), 0)

    def test_update_category_route_fail(self):
        res = self.client().patch('/categories/', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource was not found')
        self.assertFalse(data['success'])
    
    def test_delete_category_route_pass(self):
        category = self.client().post('/categories', json={ 'name': 'test'})
        category = json.loads(category.data)
        res = self.client().delete('/categories/' + str(category['category_id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['category']['id'], category['category_id'])

    def test_delete_category_route_fail(self):
        res = self.client().delete('/categories/98723649')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])


    '''
    Tag Tests
    #########################################################
    '''
    def test_get_tags_route_pass(self):
        res = self.client().get('/tags')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['tags']), 0)
        self.assertGreater(data['total_tags'], 0)
    
    def test_get_tag_route_with_valid_id(self):
        res = self.client().get('/tags/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data), 0)
        self.assertIsNotNone(data)

    def test_get_tag_route_with_invalid_id(self):
        res = self.client().get('/tags/9823647926734')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], 'resource was not found')

    def test_add_tag_route_pass(self):
        res = self.client().post('/tags', json={ 'name': 'test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(data['tag_id'], 0)

    def test_add_tag_route_fail(self):
        res = self.client().post('/tags', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

    def test_update_tag_route_pass(self):
        res = self.client().patch('/tags/2', json={ 'name': "testtag"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['tag']), 0)

    def test_update_tag_route_fail(self):
        res = self.client().patch('/tags/', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource was not found')
        self.assertFalse(data['success'])
    
    def test_delete_tag_route_pass(self):
        tag = self.client().post('/tags', json={ 'name': 'test'})
        tag = json.loads(tag.data)
        res = self.client().delete('/tags/' + str(tag['tag_id']))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['tag']['id'], tag['tag_id'])

    def test_delete_category_route_fail(self):
        res = self.client().delete('/tags/98723649')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

    '''
    Review Tests
    #########################################################
    '''
    def test_get_reviews_route_pass(self):
        res = self.client().get('/reviews')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['reviews']), 0)
        self.assertGreater(data['total_reviews'], 0)
    
    def test_get_review_route_with_valid_id(self):
        res = self.client().get('/reviews/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data), 0)
        self.assertIsNotNone(data)

    def test_get_review_route_with_invalid_id(self):
        res = self.client().get('/reviews/9823647926734')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], 'resource was not found')

    def test_add_review_route_pass(self):
        res = self.client().post('/reviews', json={ 'review': 'test', 'reviewer': 'test test', 'product_id': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(data['review_id'], 0)

    def test_add_review_route_fail(self):
        res = self.client().post('/reviews', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

    def test_update_review_route_pass(self):
        res = self.client().patch('/reviews/2', json={ 'review': "testreview"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['review']), 0)

    def test_update_review_route_fail(self):
        res = self.client().patch('/reviews/', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource was not found')
        self.assertFalse(data['success'])

    def test_delete_category_route_fail(self):
        res = self.client().delete('/reviews/98723649')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

    def test_general_404_error(self):
        res = self.client().get('/lksf923hfocwe')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource was not found')
        self.assertFalse(data['success'])
    
    def test_general_422_error(self): 
        res = self.client().post('/products')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])

# Excute tests
if __name__ == "__main__":
    unittest.main()