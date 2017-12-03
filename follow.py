import database
from tools import login_required, valid_args
from flask import Flask, flash, session, redirect, request, render_template, url_for

@login_required
def session_followers():
	result = "Error: get"
	args = (str(session.get('id', None)))
	if not valid_args(args):
		return 'Error: argument'
	result = database.DB.select("SELECT user_followed_id FROM public.user_follow WHERE user_follow_id = %s;", args, "all")
	followed = []
	print(result)
	if result:
		for row in result:
			followed.append(int(row[0]))

	session['user_follow'] = followed
	print("USER FOLLOW:", followed)

@login_required
def follow():
	result = "Error: get"
	if request.method == 'GET':
		args = (session['id'], int(request.args.get('user_id', None)))
		if not valid_args(args):
			return redirect(url_for('search'))

		if args[1] in session['user_follow']:
			return "Error: already followed"
		result = database.DB.insert("INSERT INTO public.user_follow (user_follow_id, user_followed_id) VALUES (%s, %s);", args)
		session['post_likes'].append(int(args[1]))
		session['follow'] += 1
		return redirect(url_for('back_to_search'))
	return str(result)

def do_unfollow(user_id):
	args = (session['id'], user_id)
	if not valid_args(args):
		return -1
	if args[1] not in session['user_follow']:
		return -2
	result = database.DB.insert("DELETE FROM public.user_follow WHERE user_follow_id = %s AND user_followed_id = %s;", args)
	#session['post_likes'].append(int(args[1]))
	session['follow'] -= 1
	return (0)

@login_required
def unfollow():
	result = "Error: get"
	if request.method == 'GET':
		args = (session['id'], int(request.args.get('user_id', None)))
		if not valid_args(args):
			return redirect(url_for('search'))

		if args[1] not in session['user_follow']:
			return redirect(url_for('search'))
		result = database.DB.insert("DELETE FROM public.user_follow WHERE user_follow_id = %s AND user_followed_id = %s;", args)
		session['post_likes'].append(int(args[1]))
		session['follow'] -= 1
		return redirect(url_for('back_to_search'))
	return str(result)

@login_required
def unfollow_blog():
	res = do_unfollow(int(request.args.get('user_id', None)))
	return redirect(url_for('blog'))

@login_required
def follows_unfollow():
	result = "Error: get"
	if request.method == 'GET':
		args = (session['id'], int(request.args.get('user_id', None)))
		if not valid_args(args):
			return redirect(url_for('my_follows'))

		if args[1] not in session['user_follow']:
			return redirect(url_for('my_follows'))
		result = database.DB.insert("DELETE FROM public.user_follow WHERE user_follow_id = %s AND user_followed_id = %s;", args)
		session['post_likes'].append(int(args[1]))
		session['follow'] -= 1
		return redirect(url_for('my_follows'))
	return str(result)

@login_required
def my_follows():
	args = (str(session['id']))
	result = database.DB.select("SELECT public.user.* FROM public.user_follow LEFT JOIN public.user ON (public.user_follow.user_followed_id = public.user.id) WHERE public.user_follow.user_follow_id = %s;", args, "all")
	return render_template('my_follows.html', users = result)

@login_required
def my_followers():
	args = (str(session['id']))
	result = database.DB.select("SELECT public.user.* FROM public.user_follow LEFT JOIN public.user ON (public.user_follow.user_follow_id = public.user.id) WHERE public.user_follow.user_followed_id = %s;", args, "all")
	return render_template('my_followers.html', users = result)