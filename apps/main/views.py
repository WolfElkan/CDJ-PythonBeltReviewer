# - - - - - DEPENDENCIES - - - - -

from django.shortcuts import render, redirect
from .models import User, Author, Book, Review

# - - - - - HELPER FUNCTIONS - - - - -

# Function for initializing session variables.
def seshinit(request, sesh, val=''):
	if sesh not in request.session:
		request.session[sesh] = val

def first(arr):
	if len(arr) == 0:
		return None
	else:
		return arr[0]

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
		pass
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
		return users_create(request)
	else:
		print "HACKER ALERT"
		return index(request)

def users_create(request):
	pass

def login(request):
	me = first(User.objects.filter(email=request.POST['email']))
	if me:
		request.session['log']['email']['e'] = ""

	else:
		request.session['log']['email']['e'] = "You do not have an account. Please Register."
		request.session['reg']['email']['p'] = request.POST['email']
		request.session['reg']['password']['p'] = request.POST['password']
	return entrance_get(request)
