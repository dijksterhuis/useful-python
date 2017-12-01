class SQLStatement:
	"""
	Object to handle bulding SQL queries from keyword argument/text inputs
	---------------------------------------
	Usage:
	>>> foo = SQLStatement()
	>>> foo.query()
	''
	>>> foo.sql(INSERT_INTO= 'site_visits', VALUES = (('visit_id',1), ('site_url', 'http://example.com')))
	>>> foo.query()
	'INSERT INTO site_visits (visit_id, site_url) VALUES (1, http://example.com)'
	>>> foo.forget('bar:')
	True
	>>> foo.query()
	'bar:'
	>>> foo.sql(text = 'SELECT "*"')
	>>> foo.sql(FROM = 'site_visits')
	>>> foo.sql(VALUES = {'visit_id' : 1 ,  'site_url' : 'http://example.com'})
	>>> foo.query()
	'bar: SELECT "*" FROM site_visits (visit_id, site_url) VALUES (1, http://example.com)'
	>>> foo.forget()
	True
	>>> foo.query()
	''
	---------------------------------------
	SQLStatement.sql('starting string') is used to initialise the query string.
	Takes either:
	- keyword argument parameters
		- argument names as the SQL commands, argument values as query values.
		- for any commands with a space between them (e.g. INSERT INTO)...
		- ... run them with an underscore (e.g. INSERT_INTO)
	- Text input using the text positional argument.
	Strings can be built iteratively, or in one go.
	SQLStatement.query() returns the string for assignment.
	---------------------------------------
	TODO
	- Auto-capitalise keyword argument variable names (select > SELECT)
	"""
	def __init__(self,base_string=None):
		""" Initialise the string value """
		if base_string == None:
			self.query_string = ''
		else:
			self.query_string = str(base_string) + ' '
		self.structure_type_checks = [list,tuple]
		self.value_type_checks = [float,int,str,bool]
	def __mutate__(self,string_value):
		""" Mutate the current query string with a new string """
		self.query_string = self.query_string + '%s ' % string_value
		return True
	def __values_generator__(self,values,index_selection):
		""" Extract the right data from data arrays for VALUES sql command """
		for key,value in values:
			output = (key,value)
			if type(output) == str and index_selection != 0:
				# Not quite working yet
				yield '"' + '%s' % output[index_selection] + '"'
			else:
				yield '%s' % output[index_selection]
	def __sql_select__(self,key,value):
		""" SQL SELECT LOGIC """
		self.__mutate__(key)
		if type(value) in self.structure_type_checks:
			value_string = ', '.join(map(str,value))
			self.__mutate__(value_string)
		elif type(value) in self.value_type_checks:
			self.__mutate__(value)
		#else:
		#	TYPE ERROR
	def __sql_values__(self,key,value):
		""" SQL VALUES LOGIC """
		if type(value) == dict:
			name_string, value_string = tuple(', '.join([s for s in self.__values_generator__(value.items(),i)]) for i in range(0,2))
			self.__mutate__( '(%s)' % name_string + ' %s ' % key + '(%s)' % value_string)
		elif type(value) in self.structure_type_checks:
			name_string, value_string = tuple(', '.join([s for s in self.__values_generator__(value,i)]) for i in range(2))
			self.__mutate__('(%s)' % name_string + ' %s ' % key + '(%s)' % value_string)
		elif type(value) in self.value_type_checks:
			self.__mutate__(value)
		#else:
		#	TYPE ERROR
	def __sql_where__(self,key,value):
		""" SQL WHERE LOGIC - TODO INCOMPLETE!"""
		self.__mutate__(key)
		if type(value) == dict:
			value_string = ', '.join([str(k) + ' = ' + str(v) for k,v in value.items()])
			self.__mutate__( value_string )
		elif type(value) in self.structure_type_checks:
			value_string = ', '.join([str(k) + ' = ' + str(v) for k,v in value])
			self.__mutate__( value_string )
		elif type(value) in self.value_type_checks:
			self.__mutate__(value)
		#else:
		#	TYPE ERROR
	def query(self,string_value=None):
		""" Return the query, slicing off extra whitespace 
		- must be sliced to allow for further text additions
		"""
		return self.query_string[0:len(self.query_string) - 1 ]
	def forget(self,base_string=None):
		""" Start over with a new string """
		if base_string == None:
			self.query_string = ''
		else:
			self.query_string = str(base_string) + ' '
		return True
	def sql(self,text=None,**kwargs):
		""" Run input data through checks and perform necessary actions """
		if text is not None:
			if type(text) in self.value_type_checks:
				self.__mutate__(text)
			#else:
			#	TYPE ERROR
		else:
			for key, value in kwargs.items():
				key = key.upper()
				if '_' in key:
					key = key.split('_')[0] + ' ' + key.split('_')[1]
				if key == 'SELECT':
					self.__sql_select__(key,value)
				elif key == 'VALUES':
					self.__sql_values__(key,value)
				elif key == 'WHERE':
					self.__sql_where__(key,value)
				else:
					self.__mutate__(key)
					self.__mutate__(value)