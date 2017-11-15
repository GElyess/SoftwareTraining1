#from database import DB as db
import database
from tools import login_required, valid_args
from flask import Flask, flash, session, redirect, request, render_template, url_for
import pprint

"""def comment_like_count():
	result = 0
	if (request.method == 'GET'):
		args = (request.args.get('comment_id'), None)
		if args[0] == None:
			return ("0")
		row = db.select("SELECT COUNT(*) FROM public.comment_like WHERE comment_id = %s;", args)
		result = row[0]
	return str(result)"""

def session_comment_likes():
	args = (str(session['id']))
	likes = []
	result = database.DB.select("SELECT comment_id FROM comment_like WHERE user_id = %s", args, "all")
	for row in result:
		likes.append(row[0])
	session['comment_likes'] = likes
	print ("COMMENT LIKES", session['comment_likes'])


@login_required
def comment_unlike():
	result = "Error: get"
	if request.method == 'GET':
		post_id= request.args.get('post_id', None)
		args = (session.get('id', None), request.args.get('comment_id', None))
		if not valid_args(args) or post_id == None:
			return ("Error: arguments")

		result = database.DB.insert("DELETE FROM public.comment_like WHERE user_id = %s AND comment_id =  %s;", args)
		return redirect(url_for('blog_comment', post_id = post_id))
	return str(result)

@login_required
def comment_like():
	result = "Error: get"
	if request.method == 'GET':
		post_id = request.args.get('post_id', None)
		args = (session.get('id', None), request.args.get('comment_id', None))
		if not valid_args(args) or post_id == None:
			return ("Error: arguments")
		if int(args[1]) in session['comment_likes']:
			return "Error: already liked"
		result = database.DB.insert("INSERT INTO public.comment_like (created_at, user_id, comment_id) VALUES (current_timestamp, %s, %s);", args)
		return redirect(url_for('blog_comment', post_id = post_id))
	return str(result)

@login_required
def delete_comment():
	result = 0
	if request.method == 'GET':
		args = (session.get('id', None), request.args.get('post_id', None))
		if not valid_args(args):
			return ("0")
		result = database.DB.insert("DELETE FROM public.comment_like WHERE user_id = %s AND comment_id = %s;", args)
	return str(result)


@login_required
def post_comment():
	result = 'Error: post'
	if request.method == 'POST':
		args = (session['id'], request.form.get('post_id', None), request.form.get('comment_content', None), 0)
		if not valid_args(args):
			return redirect(url_for('blog_comment', post_id = args[1]))
		if args[2] == "":
			return redirect(url_for('blog_comment', post_id = args[1]))
		result = database.DB.insert("INSERT INTO public.comments (user_id, post_id, comment_type, comment_content, likes) VALUES (%s, %s, current_timestamp, %s, %s);", args)
		return redirect(url_for('blog_comment', post_id = args[1]))
	return str(result)

@login_required
def update_comment():
	result = "Error: post"
	if request.method == 'POST':
		args = (request.form.get('content', None), session.get('id', None), request.form.get('comment_id', None), request.form.get('post_id', None))
		if not valid_args(args):
			return ("Error: argument")
		result = database.DB.insert("UPDATE public.comments SET comment_content = %s WHERE user_id = %s AND comment_id = %s AND post_id = %s;", args)
		return redirect(url_for('blog_comment', post_id = args[3]))
	return str(result)

@login_required
def delete_comment():
	result = 'Error: get'
	if request.method == 'GET':
		args = (session.get('id', None), request.args.get('comment_id', None), request.args.get('post_id', None))
		if not valid_args(args):
			return ("Error: argument")
		result = database.DB.insert("DELETE FROM public.comments WHERE user_id = %s AND comment_id = %s AND post_id = %s;", args)
		return redirect(url_for('blog_comment', post_id = args[2]))
	return str(result)

def comment_array(post_id):
	#post_id = str(post_id)
	args = (post_id,)
	result = database.DB.select("SELECT public.comments.*, public.user.name FROM public.comments LEFT JOIN public.user ON public.user.id = public.comments.user_id WHERE public.comments.post_id = %s ORDER BY public.comments.comment_id DESC", args, "all")
	#pprint(result)
	return result

#@login_required
def comments():
	result = database.DB.select("SELECT public.comments.*, public.user.name FROM public.comments LEFT JOIN public.user ON public.user.id = public.comments.user_id", (), "all")
	#pprint(result)
	return str(result)