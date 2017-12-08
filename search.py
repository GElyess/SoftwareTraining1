import database
import follow
from tools import login_required, valid_args, errorDB
from flask import Flask, flash, session, redirect, request, render_template, url_for


def get_search_request(scope, name):	
	if scope == 'username':
		args = ( "%" + name + "%", session['id'])
		sql = "SELECT * FROM public.user WHERE name LIKE %s AND public.user.id != %s ORDER BY public.user.id ASC;"
	if scope == 'email':
		args = ( "%" + name + "%", session['id'])
		sql = "SELECT * FROM public.user WHERE email LIKE %s AND public.user.id != %s ORDER BY public.user.id ASC;"
	if scope == 'both':
		args = ( "%" + name + "%", "%" + name + "%", session['id'])
		sql = "SELECT * FROM public.user WHERE (name LIKE %s OR email LIKE %s) AND public.user.id != %s ORDER BY public.user.id ASC;"
	return (sql, args)

"""@login_required
def search_all():
	args = (str(session['id']),)
	sql = "SELECT * FROM public.user WHERE public.user.id != %s ORDER BY public.user.name LIMIT 10;"
	result = database.DB.select(sql, args, "all")
	args = (session['id'],)
	followed = database.DB.select("SELECT public.user.* FROM public.user_follow LEFT JOIN public.user ON (public.user_follow.user_followed_id = public.user.id) WHERE public.user_follow.user_follow_id = %s;", args, "all")
	if result == -1 or followed == -1:
		return errorDB
	return render_template('search.html', users = result, followed = followed)"""

@login_required
def back_to_search():
	follow.session_followers()
	args = (session['id'],)
	followed = database.DB.select("SELECT public.user.* FROM public.user_follow LEFT JOIN public.user ON (public.user_follow.user_followed_id = public.user.id) WHERE public.user_follow.user_follow_id = %s;", args, "all")
	if followed == -1:
		return errorDB
	if session.get('searchparams', None) == None:
		render_template('search.html', users = 0, followed = followed)
	name = session['searchparams']['name']
	scope = session['searchparams']['scope']
	sql = get_search_request(scope, name)
	result = database.DB.select(sql[0], sql[1], "all")
	if result == -1:
		return errorDB
	return render_template('search.html', users = result, followed = followed)

@login_required
def search():
	follow.session_followers()
	scope = request.args.get('by', None)
	name = request.args.get('name', None)

	args = (session['id'],)
	followed = database.DB.select("SELECT public.user.* FROM public.user_follow LEFT JOIN public.user ON (public.user_follow.user_followed_id = public.user.id) WHERE public.user_follow.user_follow_id = %s;", args, "all")
	if scope == None or scope == 'none' or name == None or name == "":
		result = 0
	else:
		sql = get_search_request(scope, name)
		session['searchparams'] = {"scope" : scope, "name" : name}
		result = database.DB.select(sql[0], sql[1], "all")
	if followed == -1 or result == -1:
		return errorDB
	return render_template('search.html', users = result, followed = followed)

@login_required
def search_user():
	return render_template('search.html')
