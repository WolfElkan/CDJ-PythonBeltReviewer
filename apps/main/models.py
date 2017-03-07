from __future__ import unicode_literals
from django.db import models
from . import supermodel as sm

# Create your models here.

class UserManager(models.Manager):
	def __init__(self):
		self.name   = 'objects'
		self._db    = None
		self._hints = {}
		self.validations = [
			sm.Validation('name'    , r'.+'      , "Please enter your name"),
			sm.Validation('name'    , r'^.{,40}$', "Name is too long.  Max is 40 characters"),
			sm.Validation('alias'   , r'.+'      , "Please enter an alias"),
			sm.Validation('alias'   , r'^.{,40}$', "Alias is too long.  Max is 40 characters"),
			sm.Validation('email'   , r'.+'      , "Please enter your email address"),
			sm.Validation('email'   , r'^[\w+-.]+@[\w+-.]+\.[\w]+$', "Email is not valid."),
			sm.Validation('password', r'.{8,}'   , "Password should be at least 8 characters"),
			sm.Confirmation('password_conf','password',"Passwords do not match")
		]
	def isValid(self, data):
		valid = True
		for v in self.validations:
			valid &= v.isValid(data)
		return valid
	def errors(self, data, field=None):
		messages = []
		for v in self.validations:
			if field == v.field or field == None:
				messages = v.errors(data, messages)
		return messages

class User(models.Model):
	name = models.CharField(max_length=40)
	alias = models.CharField(max_length=40)
	email = models.EmailField(max_length=40)
	pw_hash = models.CharField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Author(models.Model):
	name = models.CharField(max_length=40)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class BookManager(models.Manager):
	def __init__(self):
		self.name   = 'objects'
		self._db    = None
		self._hints = {}
		self.validations = [
			sm.Validation('title', r'^.{,40}$', "Title is too long.  Max 40 characters"),
			sm.Validation('author', r'^.{,40}$', "Title is too long.  Max 40 characters"),
		]
	def isValid(self, data):
		valid = True
		for v in self.validations:
			valid &= v.isValid(data)
		return valid
	def errors(self, data, field=None):
		messages = []
		for v in self.validations:
			if field == v.field or field == None:
				messages = v.errors(data, messages)
		return messages

class Book(models.Model):
	title = models.CharField(max_length=40)
	author = models.ForeignKey(Author)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = BookManager()

class Review(models.Model):
	review = models.TextField()
	rating = models.PositiveSmallIntegerField()
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def stars(self):
		result = ""
		for x in xrange(self.rating):
		 	result += "&#x2b50; "
		return result

