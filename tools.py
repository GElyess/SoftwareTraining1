from hashlib import md5
import re
from functools import wraps
from flask import Flask, flash, session, redirect, request, render_template, url_for

errorDB = "Database unreachable"

def MD5(string):
	h = md5()
	h.update(string.encode('utf-8'))
	return h.hexdigest()

def matches(string, regex):
	if not string:
		return False
	pattern = re.compile(regex)
	match = pattern.match(string)
	if match:
		return True
	return False

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

def valid_args(args):
	for arg in args:
		if arg == None:
			return (False)
	return True