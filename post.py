#from database import DB as db
import database
import follow
from tools import login_required, valid_args
from flask import Flask, flash, session, redirect, request, render_template, url_for

"""def post_like_count():
	result = 0
	if (request.method == 'GET'):
		args = (request.args.get('post_id'), None)
		if args[0] == None:
			return ("0")
		row = db.select("SELECT COUNT(*) FROM public.post_like WHERE post_id = %s;", args)
		result = row[0]
	return str(result)"""

def session_post_likes():
	args = (str(session['id']))
	likes = []
	result = database.DB.select("SELECT post_id FROM post_like WHERE user_id = %s", args, "all")
	for row in result:
		likes.append(row[0])
	session['post_likes'] = likes
	print ("POST LIKES",likes)


@login_required
def post_like():
	result = "Error: get"
	if request.method == 'GET':
		args = (str(session.get('id', None)), request.args.get('post_id', None))
		if not valid_args(args):
			return 'Error: argument'
		print ("POST ID=", args[1])
		print(session['post_likes'])

		if int(args[1]) in session['post_likes']:
			return "Error: already liked"
		result = database.DB.insert("INSERT INTO public.post_like (created_at, user_id, post_id) VALUES (current_timestamp, %s, %s);", args)
		session['post_likes'].append(int(args[1]))
		return redirect(url_for('blog'))
	return str(result)

#@login_required
def post_unlike():
	result = "Error: get"
	if request.method == 'GET':
		args = (session.get('id', None), request.args.get('post_id', None))
		if not valid_args(args):
			return 'Error: argument'
		result = database.DB.insert("DELETE FROM public.post_like WHERE user_id = %s AND post_id = %s;", args)
		print("POST UNLIKE: post_id=", args[1], "ET mes likes=", session['post_likes'])
		if int(args[1]) in session['post_likes']:
			print("MATCH!!!")
			session['post_likes'].remove(int(args[1]))
			print("RETIRE: ", session['post_likes'])
		return redirect(url_for('blog'))
	return str(result)

@login_required
def post_add():
	result = "error post"
	if request.method == 'POST':
		args = (session.get('id', None), request.form.get('content', None), 0, 0)
		if not valid_args(args):
			return "ERROR: invalid argument"
		if args[1] == "":
			return redirect(url_for('blog'))
		result = database.DB.insert("INSERT INTO public.posts (user_id, post_content, post_time, likes, post_comments_number) VALUES (%s, %s, current_timestamp, %s, %s);", args)
		if result == 0:
			return "ERROR: insertion"
		print (type(session['posts_number']))
		session['posts_number'] += 1
		return redirect(url_for('blog'))

	return str(result)

@login_required
def post_edit():
	result = "Error: post"
	if request.method == 'POST':
		args = (request.form.get('content', None), session.get('id', None), request.form.get('post_id', None))
		if not valid_args(args):
			return 'ERROR: arguments'
		result = database.DB.insert("UPDATE public.posts SET post_content = %s WHERE user_id = %s AND post_id = %s;", args)
		if result != 1:
			return 'ERROR: insertion'
		return redirect(url_for('blog'))
	return result
#I change this function
#--johnny--
@login_required
def post_delete():
	result = "ERROR: get"
	if request.method == 'GET':
		args = (session.get('id', None), request.args.get('post_id', None))
		if not valid_args(args):
			return '0'
		#--johnny--
		#just delete comment before delete post is OK


		"""database.DB.insert("DELETE FROM public.comment_like WHERE comment_id = (SELECT public.comments.comment_id FROM public.comments WHERE public.comments.post_id = " + request.args['post_id'] + ");")

		result0 = database.DB.insert("DELETE FROM public.post_like WHERE post_id = "+ request.args['post_id'] +";", None)

		result0 = database.DB.insert("DELETE FROM public.comments WHERE user_id = %s AND post_id =  %s;", args)"""
		#
		#
		result = database.DB.insert("DELETE FROM public.posts WHERE user_id = %s AND post_id = %s;", args)
		if result != 1:
			return 'ERROR: deletion'
		return redirect(url_for('blog'))
	return str(result)

def post_array():
	result = database.DB.select("SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id ORDER BY public.posts.post_id DESC", (), "all")
	follow.session_followers()
	id_string = "("
	for follower in session['user_follow']:
		id_string = id_string + str(follower) + ","
	id_string = id_string + str(session['id']) + ")"

	sql = "SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id "
	sql += "WHERE public.posts.user_id IN " + id_string + "ORDER BY public.posts.post_time DESC"
	result = database.DB.select(sql, None, "all")
	return result

@login_required
def posts():
	result = database.DB.select("SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id ORDER BY public.posts.post_id DESC", (), "all")
	return str(result)

@login_required
def post_user():
	args = (str(request.args.get('user_id', None)))
	sql = "SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id WHERE public.posts.user_id = "
	sql += args[0]
	sql += " ORDER BY public.posts.post_time DESC"
	print("ARGS:", args)
	if not valid_args(args):
		return redirect(url_for('dashboard'))
	result = database.DB.select(sql, None, "all")
	#result = database.DB.select("SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id WHERE public.posts.user_id = %s ORDER BY public.posts.post_time DESC", args, "all")
	#print(result)
	return render_template('user_posts.html', posts = result)

@login_required
def post_mine_and_followed():
	follow.session_followers()
	id_string = "("
	for follower in session['user_follow']:
		id_string = id_string + str(follower) + ","
	id_string = id_string + str(session['id']) + ")"

	sql = "SELECT public.posts.*, public.user.name FROM public.posts LEFT JOIN public.user ON public.user.id = public.posts.user_id "
	sql += "WHERE public.posts.user_id IN " + id_string + "ORDER BY public.posts.post_time DESC"
	result = database.DB.select(sql, None, "all")
	return render_template('post_user_and_follow.html', posts = result)