import unittest
from unittest import mock
from flask import Flask
import app
import database
import os
import tempfile
import requests
import urllib

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        database.NewConn("dbname='project_training' user='postgres' password='root' host='localhost' port='5432'")
        #database.NewConn("dbname='weibo' user='postgres' password='ss5122195' host='localhost' port='5432'")

        #DB.select("SELECT post_id from public.posts WHERE post_id = 1;")

        #app.init_db()

    def tearDown(self):
        database.DB.close()
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    #get Http status code
    def get_status(self,url):
        return requests.get(url).status_code

    #welcome page's test
    def test_welcome(self):
        rv = self.app.get('/')
        url = 'http://127.0.0.1:5000/'
        status = self.get_status(url)
        assert status ==200

    def test_register(self):
        rv = self.app.post('/register', data=dict(
            username="johnnyTEST",
            password="asd12345",
            email="aaaaaaa@gg.com"
        ))
        print("TEST REGISTER STATUS CODE:",rv.status_code)
        assert rv.status_code == 200
        

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ))

    #test login page
    def test_login(self):
        #url = 'http://127.0.0.1:5000/login'
        #status = self.get_status(url)
        #print('###########################')
        #print(status)
        rv = self.login('johnnyTEST', 'asd12345')
        status = rv.status_code
        print("TEST LOGIN:", rv.status_code)
        assert status == 200

    #test blog page
    def test_login_blog(self):
        self.login('johnnyTEST', 'asd12345')
        rv = self.app.get('/blog')
        url = 'http://127.0.0.1:5000/blog'
        status = self.get_status(url)

        assert "Write" in str(rv.data) and status == 200

    # test blog page with a wrong user and password
    # def test_wrong_login_blog(self):
    #     self.login('xxd21e12rewg@$%^7', '@$#%^&*DTFGHJK')
    #     rv = self.app.get('/blog')
    #     url = 'http://127.0.0.1:5000/blog'
    #     status = self.get_status(url)
    #     print("###################")
    #     print(status)
    #     assert status == 404
        #assert "Error: Invalid Credentials. Please try again." in str(rv.data)



    #test logout function
    def test_logout(self):
        self.login('johnnyTEST', 'asd12345')
        rv = self.app.get('/logout',follow_redirects=True)
        url = 'http://127.0.0.1:5000/logout'
        status = self.get_status(url)
        assert "You are logged out" in str(rv.data) and status ==200
        
    #test register
    def register(self, username,email, password):
        return self.app.post('/register', data=dict(
            username=username,
            email = email,
            password=password
        ), follow_redirects=True)

    """def test_register(self):
          #fields = (request.form.get('username', None), request.form.get('email', None), request.form.get('password', None))
        rv = self.register('johnnytest','johnnytest@qq.com','asd12345')
        url = 'http://127.0.0.1:5000/register'
        status = self.get_status(url)
        assert "Please login" in str(rv.data) and status == 200
        database.DB.insert("DELETE FROM public.user WHERE name = 'johnnytest'")"""



    def post(self,id,content):
        return self.app.post('/post/post', data=dict(
            id = id,
            content=content,
        ), follow_redirects=True)

    def delete_post(self,id):
        return self.app.post('/post/delete?post_id=%s'%id)
    #test a post
    def test_post(self):
        self.login('johnnyTEST','asd12345')
        rv = self.post(1,'content test66666666666666666')
        #print('###################################', str(rv.data))
        assert 'content test66666666666666666' in str(rv.data)
        database.DB.insert("DELETE FROM public.posts WHERE post_content = 'content test66666666666666666'")
        #database.DB.select("SELECT post_id FROM public.posts WHERE post_content = 'content test66666666666666666')


    # test insert a new user in DB
    def test_DB(self):
      database.DB.insert(
          "INSERT INTO public.user (name, email, password) VALUES ('johnnytest','test@qq.com','asd12345');")

      results = database.DB.select("SELECT name FROM public.user WHERE name = %s;", ('johnnytest',))
      # print(results[0])
      self.assertEqual(results[0], 'johnnytest')
      database.DB.insert("DELETE FROM public.user WHERE name = 'johnnytest'")
      database.DB.insert("DELETE FROM public.user WHERE name = 'johnnyTEST'")

if __name__ == '__main__':
    unittest.main()
