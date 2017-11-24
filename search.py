import database
import follow
from tools import login_required, valid_args
from flask import Flask, flash, session, redirect, request, render_template, url_for

def get_search_request(scope, name):
	sql = "SELECT * FROM public.user WHERE "
	if scope == 'username':
		sql = sql + "name LIKE '%" + name + "%' "
	if scope == 'email':
		sql = sql + "email LIKE '%" + name + "%' "
	if scope == 'both':
		sql = sql + "(name LIKE '%" + name + "%' OR email LIKE '%" + name +"%') "
	sql = sql + "AND public.user.id != " + str(session['id']) + " ORDER BY public.user.id ASC;"
	return sql

@login_required
def search_all():
	args = (str(session['id']))
	sql = "SELECT * FROM public.user WHERE public.user.id != %s ORDER BY public.user.id;"
	result = database.DB.select(sql, args, "all")
	return render_template('search.html', users = result)

@login_required
def back_to_search():
	follow.session_followers()
	if session.get('searchparams', None) == None:
		return search_all()
	name = session['searchparams']['name']
	scope = session['searchparams']['scope']
	sql = get_search_request(scope, name)
	result = database.DB.select(sql, None, "all")
	return render_template('search.html', users = result)

@login_required
def search():
	follow.session_followers()
	scope = request.args.get('by', None)
	name = request.args.get('name', None)
	if scope == None or scope == 'none' or name == None or name == "":
		return search_all()
	else:
		sql = get_search_request(scope, name)
		session['searchparams'] = {"scope" : scope, "name" : name}
		print("SQL:", sql)
		result = database.DB.select(sql, None, "all")
		print("SEARCH RESULT:", result)
	return render_template('search.html', users = result)

@login_required
def search_user():
	return render_template('search.html')
