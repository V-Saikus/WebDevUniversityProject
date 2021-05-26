import unittest
import json
import urllib3
from flask_testing import TestCase
from launch import *
from tests.test_user import *
import base64


class MySecondTest(TestCase):
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

    def test_post_audience(self):
        user_test = MyTest()
        user_test.test_post_user()
        with app.test_client() as client:
            error_response = client.post(
                '/audience',
                headers={'Content-Type': 'something',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(error_response.status_code, 400)
            data = {'name': 'audience',
                    'price_for_hour': 100,
                    'user_id': 1,
                    }
            encoded_data = json.dumps(data).encode('utf-8')
            response = client.post(
                '/audience',
                data=encoded_data,
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(response.status_code, 201)

    def test_get_all_audiences(self):
        with app.test_client() as client:
            self.assertEqual(client.get('/audience', ).status_code, 404)
        self.test_post_audience()
        with app.test_client() as client:
            response = client.get(
                '/audience',
            )
            self.assertEqual(response.status_code, 200)

    def test_get_audience_by_id(self):
        with app.test_client() as client:
            self.assertEqual(client.get('/audience/smth', ).status_code, 400)
        self.test_post_audience()
        with app.test_client() as client:
            self.assertEqual(client.get('/audience/2', ).status_code, 404)
            response = client.get(
                '/audience/1',
            )
            self.assertEqual(response.status_code, 200)

    def test_update_audience(self):
        self.test_post_audience()
        with app.test_client() as client:
            data = {'name': 'audience',
                    'price_for_hour': 100,
                    'user_id': 1,
                    }
            encoded_data = json.dumps(data).encode('utf-8')
            response = client.put(
                '/audience/1',
                data=encoded_data,
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            data1 = {}
            encoded_data1 = json.dumps(data1).encode('utf-8')
            invalid_body_response = client.put(
                '/audience/1',
                data=encoded_data1,
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(client.put('/audience/2',
                                        headers={'Content-Type': 'application/json',
                                                 'Authorization': 'Basic ' + base64.b64encode(
                                                     'example18@mail.com:qwerty'.encode()).decode()}).status_code, 404)
            self.assertEqual(response.status_code, 202)
            self.assertEqual(invalid_body_response.status_code, 404)


# if __name__ == '__main__':
#     unittest.main()
