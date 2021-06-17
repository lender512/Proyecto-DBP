# project/test_basic.py
 
import os
import unittest
import json
from app import app, db
 
TEST_DB = 'test.db'
 
class BasicTests(unittest.TestCase):
 
############################
#### setup and teardown ####
############################
 
# executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pnpgzwyvgxkqsq:c679eba76897107ff58e453bd485504045037c91c313f328e8dcd0939e7955da@ec2-3-234-85-177.compute-1.amazonaws.com:5432/d83bs9vmmebtt8'
        #os.path.join(app.config['BASEDIR'], TEST_DB)
        
        db.drop_all()
        db.create_all()
    
    
    # executed after each test
    def tearDown(self):
        pass
    
    ###############
    #### tests ####
    ###############
    
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signIn_wrong_name(self):
        tester = app.test_client(self)
        response = tester.post(
            '/signIn', 
            data=json.dumps(dict(name='', email='luis@gmail.com', password='12345678', checkPassword='12345678')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Please write a valid name', response.data)

    def test_signIn_wrong_email(self):
        tester = app.test_client(self)
        response = tester.post(
            '/signIn', 
            data=json.dumps(dict(name='luis', email='', password='12345678', checkPassword='12345678')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Please write a valid email', response.data)

    def test_signIn_wrong_password_short(self):
        tester = app.test_client(self)
        response = tester.post(
            '/signIn', 
            data=json.dumps(dict(name='luis', email='luis@gmail.com', password='123', checkPassword='12345678')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Password must have at least 8 characters', response.data)

    def test_signIn_wrong_password(self):
        tester = app.test_client(self)
        response = tester.post(
            '/signIn', 
            data=json.dumps(dict(name='luis', email='luis@gmail.com', password='', checkPassword='12345678')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Please write a valid password', response.data)

    def test_signIn_wrong_password_match(self):
        tester = app.test_client(self)
        response = tester.post(
            '/signIn', 
            data=json.dumps(dict(name='luis', email='luis@gmail.com', password='87654321', checkPassword='12345678')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Passwords do not match', response.data)

    def test_logIn_right(self):
        tester = app.test_client(self)
        response = tester.post(
            '/logIn', 
            data=json.dumps(dict(email='luis@gmail.com', password='12345678')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'false', response.data)
    
    def test_logIn_wrong_email(self):
        tester = app.test_client(self)
        response = tester.post(
            '/logIn', 
            data=json.dumps(dict(email='', password='12345678')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Invalid email', response.data)

    def test_logIn_wrong_password(self):
        tester = app.test_client(self)
        response = tester.post(
            '/logIn', 
            data=json.dumps(dict(email='luis@gmail.com', password='')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Invalid password', response.data)

    def test_loginButton(self):
        tester = app.test_client(self)
        response = tester.get('/logInButton', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_signinButton(self):
        tester = app.test_client(self)
        response = tester.get('/signInButton', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_create_post_wrong(self):
        tester = app.test_client(self)
        response = tester.post(
            '/post/create', 
            data=json.dumps(dict(comment='asdafagaf', address='asdadadadad')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Something went wrong', response.data)

    def test_create_post_wrong_address(self):
        tester = app.test_client(self)
        response = tester.post(
            '/post/create', 
            data=json.dumps(dict(comment='hola', address='')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Create or select an address first', response.data)

    def test_create_post_wrong_address(self):
        tester = app.test_client(self)
        response = tester.post(
            '/post/create', 
            data=json.dumps(dict(comment='', address='1234')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Can not create empty post', response.data)

    def test_edit_post_wrong(self):
        tester = app.test_client(self)
        response = tester.post(
            '/post/edit', 
            data=json.dumps(dict(comment='1124141', post_id='1134134135')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Something went wrong', response.data)

    def test_edit_post_wrong_comment(self):
        tester = app.test_client(self)
        response = tester.post(
            '/post/edit', 
            data=json.dumps(dict(comment='', post_id='1')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Can not create empty post', response.data)

    def test_delete_post_wrong(self):
        tester = app.test_client(self)
        response = tester.delete(
            '/post/delete', 
            data=json.dumps(dict(post_id='5651654621')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Something went wrong', response.data)

    def test_upvote_post_wrong(self):
        tester = app.test_client(self)
        response = tester.post(
            '/post/upvote', 
            data=json.dumps(dict(post_id='5651654621')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Something went wrong', response.data)

    def test_create_apartment_wrong_district(self):
        tester = app.test_client(self)
        response = tester.post(
            '/apartments/create', 
            data=json.dumps(dict(district='', address='123')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Insert valid district', response.data)

    def test_create_apartment_wrong_address(self):
        tester = app.test_client(self)
        response = tester.post(
            '/apartments/create', 
            data=json.dumps(dict(district='surco', address='')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Insert valid address', response.data)

    def test_delete_apartment_wrong(self):
        tester = app.test_client(self)
        response = tester.delete(
            '/apartments/delete', 
            data=json.dumps(dict(apartment_id='5651654621')),
            content_type='application/json',
            follow_redirects=True)
        self.assertIn(b'Something went wrong', response.data)

    def test_search(self):
        tester = app.test_client(self)
        response = tester.get('/search/not_search', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
if __name__ == "__main__":
    unittest.main()