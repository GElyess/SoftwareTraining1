from flask import Flask, flash, session, redirect, request, render_template, url_for
#from models import db
#from models import User


#from database import NewConn, DB, test# as db
import database
from tools import *
import os
#from comment import *
import comment
import post
import search
import follow

"""TRY USING THIS"""

app = Flask(__name__)

# config
app.secret_key = os.urandom(24)
name = ""

#db = None

#app.add_url_rule('/comment_like_count', 'comment_like_count', comment.comment_like_count, methods=['GET'])
app.add_url_rule('/comment/unlike', 'comment_unlike', comment.comment_unlike, methods=['GET'])
app.add_url_rule('/comment/like', 'comment_like', comment.comment_like, methods=['GET'])
app.add_url_rule('/comment/delete', 'delete_comment', comment.delete_comment, methods=['GET'])
app.add_url_rule('/comment/post', 'post_comment', comment.post_comment, methods=['POST'])
app.add_url_rule('/comment/update', 'update_comment', comment.update_comment, methods=['POST'])
app.add_url_rule('/comment/get', 'comments', comment.comments)

#app.add_url_rule('/post_like_count', 'post_like_count', post.post_like_count, methods=['GET'])
app.add_url_rule('/post/like', 'post_like', post.post_like, methods=['GET'])
app.add_url_rule('/post/unlike', 'post_unlike', post.post_unlike, methods=['GET'])
app.add_url_rule('/post/post', 'post_add', post.post_add, methods=['POST'])
app.add_url_rule('/post/update', 'post_edit', post.post_edit, methods=['POST'])
app.add_url_rule('/post/delete', 'post_delete', post.post_delete, methods=['GET'])
app.add_url_rule('/post/get', 'posts', post.posts)
app.add_url_rule('/post/user', 'post_user', post.post_user, methods=['GET'])
#app.add_url_rule('/post/user_and_followed', 'post_mine_and_followed', post.post_mine_and_followed)

#user search
app.add_url_rule('/search', 'search', search.search)
app.add_url_rule('/back_to_search', 'back_to_search', search.back_to_search)
#app.add_url_rule('/search/user', 'search_user', )

#follow functions
app.add_url_rule('/follow', 'follow', follow.follow, methods=['GET'])
app.add_url_rule('/unfollow', 'unfollow', follow.unfollow, methods=['GET'])
app.add_url_rule('/unfollow/blog', 'unfollow_blog', follow.unfollow_blog, methods=['GET'])
app.add_url_rule('/my_follows', 'my_follows', follow.my_follows)
app.add_url_rule('/my_followers', 'my_followers', follow.my_followers)
app.add_url_rule('/follows/unfollow', 'follows_unfollow', follow.follows_unfollow, methods=['GET'])


# use decorators to link the function to a url
@app.route('/')
def home():
	if database.DB.connected == False:
		return errorDB
	return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html')

@app.route('/blog')
@login_required
def blog():
	post.session_post_likes()
	result = post.post_array()
	print('result=', result)
	return render_template('twitter.html', posts = result)

@app.route('/blog_comment', methods=['GET'])
@login_required
def blog_comment():
	comment.session_comment_likes()
	"""for i in session['comment_likes']:
		print(type(i), " ", i)"""
	result = post.post_array()
	post_id = request.args.get('post_id', None)
	if post_id == None:
		return redirect(url_for('blog'))
	check = database.DB.select("SELECT post_id from public.posts WHERE post_id = %s;", (post_id,))
	if check == -1:
		return errorDB
	if not check:
		return redirect(url_for('blog'))
	post_id = int(post_id)
	if post_id < 0:
		return redirect(url_for('blog'))
	result = comment.comment_array(str(post_id))
	if result == -1:
		return errorDB
	return render_template('comment.html', comments = result, post_id = post_id)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST': #and request.form['submit'] == 'valid':
		#cur = conn.cursor()
		fields = (request.form.get('username', None), request.form.get('email', None), request.form.get('password', None))
		if not valid_args(fields):
			return redirect(url_for('register'))

		if not matches(request.form['email'], '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$'):
			return "PATTERN ERROR EMAIL"
		
		args = (request.form['username'], request.form['email'], MD5(request.form['password']))
		res = database.DB.insert("INSERT INTO public.user (name, email, password) VALUES (%s, %s, %s);", args)
		if res == -1:
			return errorDB
		return redirect(url_for('login'))
		
	return render_template('register.html')  # render a template
   

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		args = (request.form.get('username', None), request.form.get('password', None))
		if not valid_args(args):
			print ("invalid args")
			return redirect(url_for('home'))
		args = (request.form['username'], MD5(request.form['password']))
		#print(args)
		result = database.DB.select("SELECT * FROM public.user where name = %s and password = %s;", args)
		if result == -1:
			return errorDB
		#print("RESULT=", result)
		if not result:
			error = 'Invalid Credentials. Please try again.'
			return render_template('login.html', error=error), 404
		else:
			session['logged_in'] = True
			session['id'] = result[0]
			session['name'] = result[1]
			session['email'] = result[2]
			session['password'] = result[3]
			session['gender'] = result[4]
			session['phone'] = result[5]
			session['region'] = result[7]
			session['description'] = result[8]
			session['posts_number'] = result[9]
			session['follow'] = result[10]
			session['followed'] = result[11]
			comment.session_comment_likes()
			post.session_post_likes()
			if follow.session_followers() == -1:
				return errorDB
			NAME = request.form['username']
			flash('You are logged in as ' + request.form['username'])
			name = request.form['username']
			return redirect(url_for('dashboard'))
	return render_template('login.html', error=error), 200

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are logged out.')
    return redirect(url_for('welcome'))

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
	#print("SESSION=", session)
	if request.method == 'POST':
		fields = (request.form.get('name', None), request.form.get('email', None), request.form.get('password', None), request.form.get('region', None), request.form.get('gender', None))
		if not valid_args(fields):
			return redirect(url_for('update_profile'))			

		if not matches(request.form['email'], '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$'):
			return redirect(url_for('update_profile'))
		#if not matches(request.form['password'],"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$") or len(request.form['password']) < 8:
		#	return "PARRERN ERROR PASSWORD"
		if not request.form['gender'] in ('Male', 'Female'):
			return redirect(url_for('update_profile'))


		args = (request.form['name'], request.form['email'], MD5(request.form['password']), request.form['gender'], request.form['region'], session['id'])
		result = database.DB.update("UPDATE public.user SET name = %s, email = %s, password = %s, gender = %s, user_region = %s WHERE id = %s", args)
		if result == -1:
			return errorDB
		session['name'] = request.form['name']
		session['email'] = request.form['email']
		session['password'] = request.form['password']
		session['region'] = request.form['region']
		session['gender'] = request.form['gender']
		#session['phone'] = request.form['phone']
		#session['description'] = request.form['phone']
		#return render_template('index.html')
		return redirect(url_for('dashboard'))
	return redirect(url_for('login')), 404
 
# start the server with the 'run()' method
if __name__ == '__main__':
	#database.NewConn("dbname='weibo' user='postgres' password='ss5122195' host='localhost' port='5432'")
	database.NewConn("dbname='weibo' user='postgres' password='ss5122195' host='localhost' port='5432'")
	app.run(debug=True)
