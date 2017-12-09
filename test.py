import unittest
from unittest import mock
from flask import Flask
import app
from database import NewConn,DB
import os
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        NewConn("dbname='weibo' user='postgres' password='ss5122195' host='localhost' port='5432'")

        #DB.select("SELECT post_id from public.posts WHERE post_id = 1;")

        #app.init_db()

    def tearDown(self):
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
        
    #????????????????????????????????????????????
    #???I do not know how to use database here???
    #register
    # def test_register(self):
    #     DB.insert("INSERT INTO public.user (name, email, password) VALUES ('johnnytest','test@qq.com','asd12345');")
    #     print('##############-XXXXXX-###########')
    #     str1 = DB.insert("SELECT name from public.user where name = 'johnnytest'")
    #     print(str1)
    #     DB.insert("DELETE FROM public.comment_like WHERE name = 'johnnytest'")
    #     self.assertEqual(str1,'johnnytest')


if __name__ == '__main__':
    unittest.main()
