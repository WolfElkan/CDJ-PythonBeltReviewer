from __future__ import unicode_literals
from django.db import models
from . import supermodel

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=40)
	alias = models.CharField(max_length=40)
	email = models.EmailField(max_length=40)
	pw_hash = models.CharField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Author(models.Model):
	name = models.CharField(max_length=40)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
	title = models.CharField(max_length=40)
	rating = models.PositiveSmallIntegerField()
	author = models.ForeignKey(Author)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
	review = models.TextField()
	book = models.ForeignKey(Book)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)