import unittest
from unittest import mock
from flask import Flask
import app
import database
import os
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        database.NewConn("dbname='weibo' user='postgres' password='ss5122195' host='localhost' port='5432'")

        #DB.select("SELECT post_id from public.posts WHERE post_id = 1;")

        #app.init_db()

    def tearDown(self):
        database.DB.close()
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    #welcome page's test
    def test_welcome(self):
        rv = self.app.get('/')
        assert 'Please login' in str(rv.data)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    #test login page
    def test_login(self):
        rv = self.login('johnny', 'asd12345')
        assert "Welcome to your profile page !" in str(rv.data)

    #test blog page
    def test_login_blog(self):
        self.login('johnny', 'asd12345')
        rv = self.app.get('/blog')
        assert "Write" in str(rv.data)


    #test logout function
    def test_logout(self):
        self.login('johnny', 'asd12345')
        rv = self.app.get('/logout',follow_redirects=True)

        assert "You are logged out" in str(rv.data)
        
    #test register
    def register(self, username,email, password):
        return self.app.post('/register', data=dict(
            username=username,
            email = email,
            password=password
        ), follow_redirects=True)
    def test_register(self):
          #fields = (request.form.get('username', None), request.form.get('email', None), request.form.get('password', None))
        rv = self.register('johnnytest','johnnytest@qq.com','asd12345')
        assert "Please login" in str(rv.data)



    def post(self,id,content):
        return self.app.post('/post/post', data=dict(
            id = id,
            content=content,
        ), follow_redirects=True)

    #test a post
    def test_post(self):
        self.login('johnny','asd12345')
        rv = self.post(1,'content test66666666666666666')
        assert 'content test66666666666666666' in str(rv.data)



    # test insert a new user in DB
    def test_DB(self):
      database.DB.insert(
          "INSERT INTO public.user (name, email, password) VALUES ('johnnytest','test@qq.com','asd12345');")

      results = database.DB.select("SELECT name FROM public.user WHERE name = %s;", ('johnnytest',))
      # print(results[0])
      self.assertEqual(results[0], 'johnnytest')
      database.DB.insert("DELETE FROM public.comment_like WHERE name = 'johnnytest'")


if __name__ == '__main__':
    unittest.main()
