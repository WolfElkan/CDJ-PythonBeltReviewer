# - - - - - DEPENDENCIES - - - - -

from __future__ import unicode_literals
from django.db import models, connection
from datetime import datetime
import re

# - - - - - CLASSES - - - - -

class Validation(object):
	def __init__(self, field, regex, error):
		self.field = field
		self.regex = regex
		self.error = error
	def __valid(self, data):
		datum = data[self.field]
		return re.match(self.regex, datum) != None
	def isValid(self, data, andLast=True):
		return andLast and self.__valid(data)
	def errors(self, data, messages):
		if not self.__valid(data):
			messages += [self.error]
		return messages

class Confirmation(object):
	def __init__(self, field, other, error):
		self.field = field
		self.other = other
		self.error = error
	def __valid(self, data):
		return data[self.field] == data[self.other]
	def isValid(self, data, andLast=True):
		return andLast and self.__valid(data)
	def errors(self, data, messages):
		if not self.__valid(data):
			messages += [self.error]
		return messages

# class Confirmation(Validation):
# 	def __init__(self, field, regex, error):
# 		super(Confirmation, self).__init__(field, regex, error)
# 	def __valid(self, data):
# 		print 29
# 		print data[self.field]
# 		print data[self.regex]
# 		return data[self.field] == data[self.regex]

class Field(object):
	def __init__(self, fields_array, name, data_type, *validations):
		kwargs = ""
		chars = re.search(r'(?<=[Cc]har)\d*',data_type)
		if chars:
			kwargs = "max_length={}".format(chars.group())
			data_type = "Char"
		column = "{}=models.{}Field({})".format(name, data_type, kwargs)
		exec(column)
		fields_array += [self]

class Manager(models.Manager):
	def __init__(self, app, table, fields, validations):
		self.name   = 'objects'
		self._db    = None
		self._hints = {}
		self.table_name  = app + '_' + table
		self.fields      = fields
		self.validations = validations
		create_sql = "INSERT INTO %s (" % self.table_name
		for f in fields:
			create_sql += f + ', '
		create_sql += "created_at, updated_at) VALUES ('"
		self.create_sql = create_sql
	def isValid(self, data):
		valid = True
		for x in self.validations:
			datum = data[x.field]
			valid = x.isValid(datum, valid)
		return valid
	def errors(self, data):
		messages = []
		for x in self.validations:
			datum = data[x.field]
			messages = x.errors(datum, messages)
		return messages
	# def create(self, **data):
	# 	if self.isValid(data):
	# 		sql = self.create_sql
	# 		for f in self.fields:
	# 			sql += data[f] + "', '"
	# 		sql += "{}', '{}')".format(datetime.now(),datetime.now())
	# 		print "SQL:", sql
	# 		connection.cursor().execute(sql)
	# def get(self, **crit):
	# 	result = filter(self, crit)
	# 	return False if len(result) == 0 else result[0]
	# def filter(self, **crit):
	# 	pass
	# def update(self, id, **patch):
	# 	pass
	# def delete(self, id):
	# 	pass

# class Email(models.Model):
# 	Field('email','Char',45)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)

# 	validations = [
# 		Validation('email',r'^[\w.+-]+@[\w.+-]+\.[a-zA-Z]+$',"Email is not valid!"),
# 		Validation('email',r'^.{,45}$',"Email is too long"),
# 	]
# 	objects = Manager('main','Email',['email'],validations)




