#from database import DB as db
import database
from tools import login_required, valid_args, errorDB
from flask import Flask, flash, session, redirect, request, render_template, url_for, Response

OK = 302
ERROR = 304

def session_comment_likes():
	args = (session['id'],)
	likes = []
	result = database.DB.select("SELECT comment_id FROM comment_like WHERE user_id = %s", args, "all")
	if result == -1:
		return
	if type(result) != type(int):
		for row in result:
			likes.append(row[0])
		session['comment_likes'] = likes

@login_required
def comment_unlike():
	result = "Error: get"
	status_code = OK
	if request.method == 'GET':
		post_id= request.args.get('post_id', None)
		args = (session.get('id', None), request.args.get('comment_id', None))
		if not valid_args(args) or post_id == None:
			return ("Error: arguments"), 400

		result = database.DB.insert("DELETE FROM public.comment_like WHERE user_id = %s AND comment_id =  %s;", args)
		if result == -1:
			return errorDB, 500
		if result != 1:
			return "comment not found", 404
		session_comment_likes()
		"""if args[1] in session['comment_likes']:
			session['comment_likes'].remove(args[1])"""
		return "comment " + args[1] + " liked", 200
		#return redirect(url_for('blog_comment', post_id = post_id)), status_code
	return str(result), 405

@login_required
def comment_like():
	result = "Error: get"
	status_code = OK
	if request.method == 'GET':
		post_id = request.args.get('post_id', None)
		args = (session.get('id', None), request.args.get('comment_id', None))
		if not valid_args(args) or post_id == None:
			return ("Error: arguments"), 400
		if int(args[1]) in session['comment_likes']:
			return "Error: already liked", 400
		result = database.DB.insert("INSERT INTO public.comment_like (user_id, comment_id) VALUES (%s, %s);", args)
		session_comment_likes()
		#session['comment_likes'].append(args[1])
		if result == -1:
			return errorDB, 500
		if result != 1:
			return "comment not found", 404
		return "comment " + args[1] + " liked", 200
		#return redirect(url_for('blog_comment', post_id = post_id)), status_code
	return str(result), 405

"""@login_required
def delete_comment():
	result = 0
	status_code = 200
	if request.method == 'GET':
		args = (session.get('id', None), request.args.get('post_id', None))
		if not valid_args(args):
			return ("0")
		result = database.DB.insert("DELETE FROM public.comment_like WHERE user_id = %s AND comment_id = %s;", args)
		if result == -1:
			return errorDB
		if result != 1:

	return str(result)"""


@login_required
def post_comment():
	result = 'Error: post'
	status_code = OK
	if request.method == 'POST':
		post_id = request.form.get('post_id', None)
		args = (session['id'], post_id, request.form.get('comment_content', None),)
		if not valid_args(args):
			return "invalid arguments", 400

		if args[2] == "":
			return "no comment content", 400
		result = database.DB.insert("INSERT INTO public.comments (user_id, post_id, comment_content) VALUES (%s, %s, %s);", args)
		if result == -1:
			return errorDB, 500
		if result != 1:
			return "insertion failed", 404

		args = (post_id,)
		result = database.DB.select("SELECT public.comments.*, public.user.name FROM public.comments LEFT JOIN public.user ON public.user.id = public.comments.user_id WHERE public.comments.post_id = %s ORDER BY public.comments.created_at DESC", args)
		if result == -1:
			return errorDB, 500
		return render_template('single_comment.html', post_id=post_id, comment=result), 200
	return str(result), 405

@login_required
def update_comment():
	result = "Error: post"
	status_code = OK
	if request.method == 'POST':
		args = (request.form.get('content', None), session.get('id', None), request.form.get('comment_id', None), request.form.get('post_id', None))
		if not valid_args(args):
			return ("Error: argument"), 400
		if args[0] == "":
			return "Empty content", 400
		result = database.DB.insert("UPDATE public.comments SET comment_content = %s WHERE user_id = %s AND comment_id = %s AND post_id = %s;", args)
		if result == -1:
			return errorDB, 500
		if result != 1:
			return "comment not found.", 404
		return ("comment " + args[2] + " updated"), 200
	return str(result), 400

@login_required
def delete_comment():
	result = 'Error: get'
	if request.method == 'GET':
		args = (session.get('id', None), request.args.get('comment_id', None), request.args.get('post_id', None))
		if not valid_args(args):
			return ("Error: argument"), 400
		result = database.DB.insert("DELETE FROM public.comments WHERE user_id = %s AND comment_id = %s AND post_id = %s;", args)
		if result == -1:
			return errorDB, 500
		if result != 1:
			return "comment not found", 404
		return "comment deleted", 200
		#return redirect(url_for('blog_comment', post_id = args[2])), status_code
	return str(result), 405

def comment_array(post_id):
	args = (post_id,)
	result = database.DB.select("SELECT public.comments.*, public.user.name FROM public.comments LEFT JOIN public.user ON public.user.id = public.comments.user_id WHERE public.comments.post_id = %s ORDER BY public.comments.created_at DESC", args, "all")
	return result

#@login_required
def comments():
	result = database.DB.select("SELECT public.comments.*, public.user.name FROM public.comments LEFT JOIN public.user ON public.user.id = public.comments.user_id", (), "all")
	return result

def comment_list():
	post_id = request.args.get('post_id', None)
	args = (str(post_id),)
	if post_id == None:
		return Response('error argument', status=400, mimetype='application/json');
	result = database.DB.select("SELECT public.comments.*, public.user.name FROM public.comments LEFT JOIN public.user ON public.user.id = public.comments.user_id WHERE public.comments.post_id = %s ORDER BY public.comments.created_at DESC", args, "all")
	#result = comment_array(str(post_id))
	if result == -1:
		return Response(errorDB, status=500, mimetype='application/json')
	#return "erreur avec render_template", 200
	return render_template('comment_list.html', comments = result, post_id = post_id), 200