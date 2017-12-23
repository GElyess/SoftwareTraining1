import unittest
from unittest import mock
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

        #DB.select("SELECT post_id from public.posts WHERE post_id = 1;")

        #app.init_db()

    def tearDown(self):
        database.DB.insert("DELETE FROM public.posts WHERE post_content = 'content test66666666666666666'")
        database.DB.insert("DELETE FROM public.posts WHERE post_content = 'content test999'")
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
        assert 'Please login' in str(rv.data) and status ==200


    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    #test login page
    def test_login(self):
        url = 'http://127.0.0.1:5000/login'
        status = self.get_status(url)
        rv = self.login('johnny', 'asd12345')
        assert status == 200

    #test blog page
    def test_login_blog(self):
        self.login('johnny', 'asd12345')
        rv = self.app.get('/blog')
        url = 'http://127.0.0.1:5000/blog'
        status = self.get_status(url)

        assert  status == 200

    #test blog page with a wrong user and password
    def test_wrong_user_and_password_login_blog(self):
        status = self.login('xxd21e12rewg@$%^7', '@$#%^&*DTFGHJK').status_code
        #print('STATUS:', status)
        assert status == 404
        rv = self.app.get('/blog')
        url = 'http://127.0.0.1:5000/blog'
        status = rv.status_code
        assert status == 302
        #assert "Error: Invalid Credentials. Please try again." in str(rv.data)

    def test_empty_user_or_password_login_blog(self):
        status = self.login(None, '@$#%^&*DTFGHJK').status_code
        assert status == 400
        rv = self.app.get('/blog')
        url = 'http://127.0.0.1:5000/blog'
        status = rv.status_code
        assert status == 302
        #assert "Error: Invalid Credentials. Please try again." in str(rv.data)



    #test logout function
    def test_logout(self):
        self.login('johnny', 'asd12345')
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

    def test_register(self):
        #fields = (request.form.get('username', None), request.form.get('email', None), request.form.get('password', None))
        rv = self.register('johnnytest','johnnytest@qq.com','asd12345')
        url = 'http://127.0.0.1:5000/register'
        status = rv.status_code
        #print('sasasasasa',status)
        assert  status == 200
        database.DB.insert("DELETE FROM public.user WHERE name = 'johnnytest'")

    def test_empty_email_register(self):
        #fields = (request.form.get('username', None), request.form.get('email', None), request.form.get('password', None))
        rv = self.register('johnnytest',None,'asd12345')
        url = 'http://127.0.0.1:5000/register'
        status = rv.status_code
        #print('sasasasasa',status)
        assert  status == 400
        database.DB.insert("DELETE FROM public.user WHERE name = 'johnnytest'")
    def test_empty_password_register(self):
        #fields = (request.form.get('username', None), request.form.get('email', None), request.form.get('password', None))
        rv = self.register('johnnytest','johnnytest@qq.com',None)
        url = 'http://127.0.0.1:5000/register'
        status = rv.status_code
        #print('sasasasasa',status)
        assert  status == 400
        database.DB.insert("DELETE FROM public.user WHERE name = 'johnnytest'")
    def test_empty_user_register(self):
        #fields = (request.form.get('username', None), request.form.get('email', None), request.form.get('password', None))
        rv = self.register(None,'johnnytest@qq.com','asd12345')
        url = 'http://127.0.0.1:5000/register'
        status = rv.status_code
        #print('sasasasasa',status)
        assert  status == 400
        database.DB.insert("DELETE FROM public.user WHERE name = 'johnnytest'")


    def post(self,id,content):
        return self.app.post('/post/post', data=dict(
            id = id,
            content=content,
        ), follow_redirects=True)

    def delete_post(self,id):
        return self.app.post('/post/delete?post_id=%s'%id)
    #test a post
    def test_post(self):
        self.login('johnny','asd12345')
        rv = self.post(1,'content test66666666666666666')
        assert 'content test66666666666666666' in str(rv.data)
        #database.DB.select("SELECT post_id FROM public.posts WHERE post_content = 'content test66666666666666666')

    def comment(self, post_id, content):
        return self.app.post('/comment/post', data=dict(
            post_id=post_id,
            comment_content=content,
        ), follow_redirects=False)

    #test comment
    def test_comment(self):
        self.login('johnny', 'asd12345')
        response = self.post(1, 'content test999')
        post_id = database.DB.select("SELECT post_id FROM public.posts WHERE post_content = 'content test999'")
        url = 'http://127.0.0.1:5000/blog_comment?post_id=%s'%post_id[0]
        url2 = 'http://127.0.0.1:5000/comment/post'
        rv = self.comment(post_id[0],'6666666')

        status = rv.status_code
        #print('test comment stqtus:', status)
        assert  status == 200

    def test_wrong_comment(self):
        self.login('johnny', 'asd12345')
        response = self.post(1, 'content test999')
        post_id = database.DB.select("SELECT post_id FROM public.posts WHERE post_content = 'content test999'")
        url = 'http://127.0.0.1:5000/blog_comment?post_id=%s'%post_id[0]
        url2 = 'http://127.0.0.1:5000/comment/post'
        rv = self.comment(post_id[0],None)
        status = rv.status_code
        #print('test comment stqtus:', status)
        assert  status == 400

    def test_like_comment(self):
        self.login('johnny', 'asd12345')
        response = self.post(1, 'content test999')
        post_id = database.DB.select("SELECT post_id FROM public.posts WHERE post_content = 'content test999'")
        post_id = post_id[0]
        self.comment(str(post_id), '6666666')
        comment_id = database.DB.select("SELECT comment_id FROM public.comments WHERE comment_content = '6666666'")
        comment_id=comment_id[0]
        #print('idididididiiddi', comment_id[0])
        #print('POST ID:', post_id[0])
        url = '/comment/like?comment_id=%s&post_id=%s'%(str(comment_id),str(post_id))
        rv=self.app.get(url)
        '''rv = self.app.get('/comment/like', data=dict(
            comment_id=comment_id[0],
            post_id= post_id[0]
        ))'''
        status = rv.status_code
        #print('#######################', status)
        assert status == 200
        # url = '/comment/unlike?comment_id=%s&post_id=%s' % (comment_id, str(post_id))
        # rv = self.app.get(url)
        # status = rv.status_code
        # print('^^^^&^^^^^^^^^^^^^^^^^', rv.data)
        # print('#######################', status)
        # #assert status == 200



    # test insert a new user in DB
    def test_DB(self):
      database.DB.insert(
          "INSERT INTO public.user (name, email, password) VALUES ('johnnytest','test@qq.com','asd12345');")

      results = database.DB.select("SELECT name FROM public.user WHERE name = %s;", ('johnnytest',))
      # print(results[0])
      self.assertEqual(results[0], 'johnnytest')
      database.DB.insert("DELETE FROM public.user WHERE name = 'johnnytest'")


if __name__ == '__main__':
    unittest.main()
