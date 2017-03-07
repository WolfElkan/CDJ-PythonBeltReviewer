# - - - - - DEPENDENCIES - - - - -

from django.shortcuts import render, redirect
from .models import User, Author, Book, Review
import bcrypt

# - - - - - HELPER FUNCTIONS - - - - -

def seshinit(request, sesh, val=''):
	if sesh not in request.session:
		request.session[sesh] = val

def forminit(request, form_name, fields):
	blank = {}
	for f in fields:
		blank[f] = {'p':"", 'e':""}
	seshinit(request, form_name, blank)

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

def select_array(model, num):
	length = model.objects.all().last().id
	array = list([""] * length)
	array[num] = "selected"

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

# - - - - - SECURITY FUNCTIONS - - - - -

def secure_session(request, user_id):
	request.session['user_id'] = user_id

def authentic(request):
	return bool(request.session['user_id'])

# - - - - - APPLICATION VIEWS - - - - -

# - - - - LOGIN & REGISTRATION - - - -

def index(request):
	seshinit(request,'user_id',None)
	if authentic(request):
		return redirect('/books')
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
	forminit(request,'log',['email','password'])
	forminit(request,'reg',['name','alias','email','password','password_conf',])
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
		users_create(request, new_user)
		return index(request)
	else:
		for f in fields:
			errors = User.objects.errors(new_user, f)
			message = ""
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

def logout(request):
	request.session.clear()
	return redirect('/')

# - - - - BOOK REVIEWS - - - -

def books_index(request):
	if not authentic(request):
		return redirect('/')
	me = User.objects.get(id = request.session['user_id'])
	context = {
		'alias'  : me.alias,
		'recent' : Review.objects.all(),
		'others' : Book.objects.all(),
	}
	return render(request, 'main/books.html', context)

def books_new(request):
	if not authentic(request):
		return redirect('/')
	elif request.method == "GET":
		return books_new_get(request)
	elif request.method == "POST":
		return books_new_post(request)
	else:
		print "Unrecognized HTTP Verb"
		return redirect('/')

def books_new_get(request):
	forminit(request,'new_book',['title','author_new','review','rating'])
	context = {
		'authors' : Author.objects.all(),
		'form' : request.session['new_book']
	}
	return render(request, 'main/books_new.html', context)

def books_new_post(request):
	me = User.objects.get(id = request.session['user_id'])
	new_author = None
	if request.POST['author_id'] != "0":
		new_author = Author.objects.get(id=int(request.POST['author_id']))
		author_valid = True
	else:
		author_valid = len(request.POST['author_new']) <= 40
	book_valid = len(request.POST['author_new']) <= 40
	rating_valid = 1 <= int(request.POST['rating']) <= 5

	if not author_valid:
		request.session['new_book']['author_new']['e'] = "Author name is too long.  Max is 40 characters"
	else:
		request.session['new_book']['author_new']['e'] = ""

	if not book_valid:
		request.session['new_book']['title']['e'] = "Book title is too long.  Max is 40 characters"
	else:
		request.session['new_book']['title']['e'] = ""

	if not rating_valid:
		request.session['new_book']['rating']['e'] = "Please add a 1-5 star rating to your review"
	else:
		request.session['new_book']['rating']['e'] = ""

	if author_valid and book_valid and rating_valid:
		if not new_author:
			new_author = Author.objects.create(name=request.POST['author_new'])
		new_book = Book.objects.create(title=request.POST['title'],author=new_author)
		new_review = Review.objects.create(
			review = request.POST['review'],
			rating = request.POST['rating'],
			book   = new_book,
			user   = me,
		)
		return redirect('/books/{}'.format(new_book.id))
	else:
		request.session['new_book']['title']     ['p'] = request.POST['title']
		request.session['new_book']['author_new']['p'] = request.POST['author_new']
		request.session['new_book']['review']    ['p'] = request.POST['review']
		return books_new_get(request)









