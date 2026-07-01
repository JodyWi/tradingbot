import unittest
from unittest.mock import patch
import requests
from flask import Flask
from luno_get_balance import app

class TestLunoAPIFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

    def test_get_balance(self):
        # Mock the requests.get method
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "balance": [
                    {"currency": "XBT", "balance": "0.0"},
                    {"currency": "ETH", "balance": "0.0"}
                ]
            }

            # Make a request to the endpoint
            response = self.client.get('/api/1/balance?assets=XBT&assets=ETH')
            
            # Assert status code and response data
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {
                "balance": [
                    {"currency": "XBT", "balance": "0.0"},
                    {"currency": "ETH", "balance": "0.0"}
                ]
            })

    def test_get_balance_error(self):
        # Mock the requests.get method to return an error
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 400
            mock_get.return_value.text = 'Bad Request'

            # Make a request to the endpoint
            response = self.client.get('/api/1/balance?assets=XBT&assets=ETH')
            
            # Assert status code and error message
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json, {"error": 'Bad Request'})

if __name__ == '__main__':
    unittest.main()
