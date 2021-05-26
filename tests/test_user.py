import unittest
import json
import urllib3
from flask_testing import TestCase
from launch import *
import base64


class MyTest(TestCase):
    def create_app(self):
        # app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.session.commit()
        db.create_all()

    def tearDown(self):
        db.session.commit()
        db.drop_all()

    def test_server_is_up_and_running(self):
        http = urllib3.PoolManager()
        url = 'http://localhost:5000/'
        response = http.request('GET', url)
        self.assertEqual(response.status, 200)

    def test_get_user_by_id(self):
        with app.test_client() as client:
            self.assertEqual(client.get('/user/smth', ).status_code, 400)
        self.test_post_user()
        with app.test_client() as client:
            self.assertEqual(client.get('/user/2', ).status_code, 404)
            response = client.get(
                '/user/1',
            )
            self.assertEqual(response.status_code, 200)

    def test_post_user(self):
        with app.test_client() as client:
            error_response = client.post(
                '/user',
                headers={'Content-Type': 'something',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(error_response.status_code, 400)
        with app.test_client() as client:
            data = {'first_name': 'first',
                    'second_name': 'second',
                    'birthday': '14.08.2002',
                    'email': 'example18@mail.com',
                    'phone_number': '0991234567',
                    'password': 'qwerty'
                    }
            encoded_data = json.dumps(data).encode('utf-8')
            response = client.post(
                '/user',
                data=encoded_data,
                headers={'Content-Type': 'application/json'}
            )
            second_response = client.post(
                '/user',
                data=encoded_data,
                headers={'Content-Type': 'application/json'}
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(second_response.status_code, 409)

    def test_update_user(self):
        self.test_post_user()
        with app.test_client() as client:
            data = {'first_name': 'first',
                    'second_name': 'ahahhah',
                    'birthday': '14.08.2002',
                    'email': 'example18@mail.com',
                    'phone_number': '0991255567',
                    'password': 'qwerty'
                    }
            encoded_data = json.dumps(data).encode('utf-8')
            response = client.put(
                '/user/1',
                data=encoded_data,
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            data1 = {}
            encoded_data1 = json.dumps(data1).encode('utf-8')
            invalid_body_response = client.put(
                '/user/1',
                data=encoded_data1,
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            invalid_user_response = client.put(
                '/user/smth',
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(response.status_code, 202)
            self.assertEqual(invalid_user_response.status_code, 404)
            self.assertEqual(invalid_body_response.status_code, 404)

#
# if __name__ == '__main__':
#     unittest.main()
