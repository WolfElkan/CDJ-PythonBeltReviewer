# - - - - - DEPENDENCIES - - - - -

from django.shortcuts import render, redirect
from .models import User, Author, Book, Review
import bcrypt

# - - - - - HELPER FUNCTIONS - - - - -

def seshinit(request, sesh, val=''):
	if sesh not in request.session:
		request.session[sesh] = val

def first(arr):
	if len(arr) == 0:
		return None
	else:
		return arr[0]

def copy(source, keys=False):
	this = {}
	if not keys:
		keys = source.keys()
	for key in keys:
		this[key] = source[key]
	return this

# - - - - - DEVELOPER VIEWS - - - - -

def hot(request):
	seshinit(request,'command')
	context = {
		# Models
		'command': request.session['command']
	}
	return render(request, "main/hot.html", context)

def run(request):
	command = request.POST['command']
	request.session['command'] = command
	exec(command)
	return redirect ('/hot')

def nuke(request):
	#.objects.all().delete()
	return redirect ('/hot')

# - - - - - APPLICATION VIEWS - - - - -

def index(request):
	seshinit(request,'user_id',None)
	if request.session['user_id']:
		return access(request)
	else:
		return entrance(request)

def entrance(request):
	if request.method == "GET":
		return entrance_get(request)
	elif request.method == "POST":
		return entrance_post(request)
	else:
		print "Unrecognized HTTP Verb"
		return index(request)

def entrance_get(request):
	seshinit(request,'log',{
		'email':         {'p':"", 'e':""},
		'password':      {'p':"", 'e':""},
	})
	seshinit(request,'reg',{
		'name':          {'p':"", 'e':""},
		'alias':         {'p':"", 'e':""},
		'email':         {'p':"", 'e':""},
		'password':      {'p':"", 'e':""},
		'password_conf': {'p':"", 'e':""},
	})
	context = {
		'log': request.session['log'],
		'reg': request.session['reg'],
	}
	return render(request, "main/entrance.html", context)

def entrance_post(request):
	if request.POST['operation'] == "Log":
		return login(request)
	elif request.POST['operation'] == "Reg":
		return register(request)
	else:
		print "HACKER ALERT"
		return index(request)

def register(request):
	fields = ['name','alias','email','password','password_conf']
	new_user = copy(request.POST,fields)
	if User.objects.isValid(new_user):
		return users_create(request, new_user)
	else:
		for f in fields:
			message = ""
			errors = User.objects.errors(new_user, f)
			for e in errors:
				if message:
					message += ", "
				message += e
			request.session['reg'][f]['e'] = message
			request.session['reg'][f]['p'] = request.POST[f]
		return entrance_get(request)

def login(request):
	me = first(User.objects.filter(email=request.POST['email']))
	if me:
		request.session['log']['email']['e'] = ""
		if bcrypt.checkpw(bytes(request.POST['password']),bytes(me.pw_hash)):
			secure_session(request, me.id)
			return index(request)
		else:
			request.session['log']['password']['e'] = "Your password is incorrect."
			request.session['log']['email']['p'] = request.POST['email']
			return entrance_get(request)
	else:
		request.session['log']['email']['e'] = "You do not have an account. Please Register."
		request.session['reg']['email']['p'] = request.POST['email']
	return entrance_get(request)

def users_create(request, new_user):
	encrypted_password = bcrypt.hashpw(bytes(new_user['password']),bcrypt.gensalt())
	me = User.objects.create(
		name    = new_user['name'],
		alias   = new_user['alias'],
		email   = new_user['email'],
		pw_hash = encrypted_password
	)
	secure_session(request, me.id)
	return index(request)

def secure_session(request, user_id):
	request.session['user_id'] = user_id

def access(request):
	print "Successfully logged in as User #{}".format(request.session['user_id'])
	return entrance_get(request)