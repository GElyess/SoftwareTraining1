#from database import DB as db
import database
import follow
from tools import login_required, valid_args, errorDB
from flask import Flask, flash, session, redirect, request, render_template, url_for

OK = 302
ERROR = 304

def session_post_likes():
	args = (str(session['id']),)
	likes = []
	result = database.DB.select("SELECT post_id FROM post_like WHERE user_id = %s;", args, "all")
	for row in result:
		likes.append(row[0])
	session['post_likes'] = likes
	#print ("POST LIKES",likes)


@login_required
def post_like():
	result = "Error: get"
	status_code = OK
	if request.method == 'GET':
		args = (str(session.get('id', None)), request.args.get('post_id', None))
		if not valid_args(args):
			return 'Error: argument'
		#print ("POST ID=", args[1])
		#print(session['post_likes'])

		if int(args[1]) in session['post_likes']:
			return "Error: already liked"
		result = database.DB.insert("INSERT INTO public.post_like (user_id, post_id) VALUES (%s, %s);", args)
		if result == -1:
			return errorDB
		if result != 1:
			status_code = ERROR
		session['post_likes'].append(int(args[1]))
		return redirect(url_for('blog')), status_code
	return str(result)

@login_required
def post_unlike():
	result = "Error: get"
	status_code = OK
	if request.method == 'GET':
		args = (session.get('id', None), request.args.get('post_id', None))
		if not valid_args(args):
			return 'Error: argument'
		result = database.DB.insert("DELETE FROM public.post_like WHERE user_id = %s AND post_id = %s;", args)
		if result == -1:
			return errorDB
		if result != 1:
			status_code = ERROR
		#print("POST UNLIKE: post_id=", args[1], "ET mes likes=", session['post_likes'])
		if int(args[1]) in session['post_likes']:
			#print("MATCH!!!")
			session['post_likes'].remove(int(args[1]))
			#print("RETIRE: ", session['post_likes'])
		return redirect(url_for('blog')), status_code
	return str(result)

@login_required
def post_add():
	result = "error post"
	status_code = 301
	if request.method == 'POST':
		args = (session.get('id', None), request.form.get('content', None),)
		if not valid_args(args):
			return "ERROR: invalid argument"
		if args[1] == "":
			return redirect(url_for('blog'))
		result = database.DB.insert("INSERT INTO public.posts (user_id, post_content) VALUES (%s, %s);", args)
		if result == -1:
			return errorDB
		if result == 0:
			status_code = 304
			return "ERROR: insertion"
		#print (type(session['posts_number']))
		session['posts_number'] += 1
		return redirect(url_for('blog'), code=status_code)
	return str(result)

@login_required
def post_edit():
	result = "Error: post"
	status_code = OK
	if request.method == 'POST':
		args = (request.form.get('content', None), session.get('id', None), request.form.get('post_id', None))
		if not valid_args(args):
			return 'ERROR: arguments'
		result = database.DB.insert("UPDATE public.posts SET post_content = %s WHERE user_id = %s AND post_id = %s;", args)
		if result == -1:
			return errorDB
		if result != 1:
			status_code = ERROR
			return 'ERROR: insertion'
		return redirect(url_for('blog')), status_code
	return result
#I change this function
#--johnny--
@login_required
def post_delete():
	result = "ERROR: get"
	status_code = OK
	if request.method == 'GET':
		args = (session.get('id', None), request.args.get('post_id', None))
		if not valid_args(args):
			return '0'
		result = database.DB.insert("DELETE FROM public.posts WHERE user_id = %s AND post_id = %s;", args)
		if result == -1:
			return errorDB
		if result != 1:
			status_code = ERROR
			#return 'ERROR: deletion'
		return redirect(url_for('blog')), status_code
	return str(result)

def post_array():
	result = database.DB.select("SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id ORDER BY public.posts.post_id DESC", (), "all")
	follow.session_followers()
	id_string = "("
	'''for follower in session['user_follow']:
		id_string = id_string + str(follower) + ","
	id_string = id_string + str(session['id']) + ")"'''
	args = (str(session['id']),)
	sql_follow = "(SELECT user_followed_id FROM public.user_follow WHERE user_follow_id = %s)"
	sql = "SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id "
	sql += "WHERE public.posts.user_id IN "+ sql_follow +" ORDER BY public.posts.post_time DESC"
	result = database.DB.select(sql, args, "all")
	return result

@login_required
def posts():
	result = database.DB.select("SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id ORDER BY public.posts.post_id DESC", (), "all")
	return str(result)

@login_required
def post_user():
	status_code = OK
	args = (str(request.args.get('user_id', None)),)
	sql = "SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id WHERE public.posts.user_id = %s  ORDER BY public.posts.post_time DESC;"
	#print("ARGS:", args)
	if not valid_args(args):
		return redirect(url_for('dashboard')), ERROR
	result = database.DB.select(sql, args, "all")
	if result == -1:
		return errorDB
	return render_template('user_posts.html', posts = result)
