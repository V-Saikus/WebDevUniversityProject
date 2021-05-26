from tests.test_audience import *
import base64


class MyThirdTest(TestCase):
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

    def test_post_reservation(self):
        audience_test = MySecondTest()
        audience_test.test_post_audience()
        with app.test_client() as client:
            error_response = client.post(
                '/audience/reserve',
                headers={'Content-Type': 'something',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(error_response.status_code, 400)
            data = {'start_time': '2020-8-14 03:30:35.166',
                    'end_time': '2020-8-14 06:30:35.166',
                    'user_id': 1,
                    'audience_id': 1,
                    }
            encoded_data = json.dumps(data).encode('utf-8')
            response = client.post(
                '/audience/reserve',
                data=encoded_data,
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(response.status_code, 201)

    def test_get_reservation_by_id(self):
        with app.test_client() as client:
            self.assertEqual(client.get('/audience/reserve/smth', ).status_code, 400)
        self.test_post_reservation()
        with app.test_client() as client:
            response = client.get(
                '/audience/reserve/1',
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(client.get('/audience/reserve/2', ).status_code, 404)

    def test_update_reservation(self):
        self.test_post_reservation()
        with app.test_client() as client:
            data = {'start_time': '2020-8-14 06:30:35.166',
                    'end_time': '2020-8-14 09:30:35.166',
                    }
            encoded_data = json.dumps(data).encode('utf-8')
            response = client.put(
                '/reserve/1',
                data=encoded_data,
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            invalid_reservation_response = client.put(
                '/reserve/smth',
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            data1 = {}
            encoded_data1 = json.dumps(data1).encode('utf-8')
            invalid_body_response = client.put(
                '/reserve/1',
                data=encoded_data1,
                headers={'Content-Type': 'application/json',
                         'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(response.status_code, 202)
            self.assertEqual(invalid_reservation_response.status_code, 404)
            self.assertEqual(invalid_body_response.status_code, 404)

    def test_delete_reservation_by_id(self):
        self.test_post_reservation()
        with app.test_client() as client:
            response = client.delete(
                '/reserve/1',
                headers={'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            invalid_reservation_response = client.delete(
                '/reserve/smth',
                headers={'Authorization': 'Basic ' + base64.b64encode('example18@mail.com:qwerty'.encode()).decode()}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(invalid_reservation_response.status_code, 404)
