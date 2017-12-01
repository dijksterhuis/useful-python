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
		""" Initialise string value """
		if base_string == None:
			self.query_string = ''
		else:
			self.query_string = str(base_string) + ' '
		self.structure_type_checks = [list,tuple]
		self.value_type_checks = [float,int,str,bool]
	def mutate(self,string_value):
		""" Mutate the current query string with a new string """
		self.query_string = self.query_string + '%s ' % string_value
		return True
	def query(self,string_value=None):
		""" Return the query, slicing off extra whitespace 
		- must be sliced to allow for further text additions
		"""
		return self.query_string[0:len(self.query_string) - 1 ]
	def forget(self,base_string=None):
		""" Reset to a new starting point """
		if base_string == None:
			self.query_string = ''
		else:
			self.query_string = str(base_string) + ' '
		return True
	def values_generator(self,values,index_selection):
		""" Extract the right data from data arrays """
		for key,value in values:
			output = (key,value)
			if type(output) == str and index_selection != 0:
				# Not quite working yet
				yield '"' + '%s' % output[index_selection] + '"'
			else:
				yield '%s' % output[index_selection]
	def sql_select(self,key,value):
		""" SQL SELECT LOGIC """
		self.mutate(key)
		if type(value) in self.structure_type_checks:
			value_string = ', '.join(map(str,value))
			self.mutate(value_string)
		elif type(value) in self.value_type_checks:
			self.mutate(value)
		#else:
		#	TYPE ERROR
	def sql_values(self,key,value):
		""" SQL VALUES LOGIC """
		if type(value) == dict:
			name_string, value_string = tuple(', '.join([s for s in self.values_generator(value.items(),i)]) for i in range(0,2))
			self.mutate( '(%s)' % name_string + ' %s ' % key + '(%s)' % value_string)
		elif type(value) in self.structure_type_checks:
			name_string, value_string = tuple(', '.join([s for s in self.values_generator(value,i)]) for i in range(2))
			self.mutate('(%s)' % name_string + ' %s ' % key + '(%s)' % value_string)
		elif type(value) in self.value_type_checks:
			self.mutate(value)
		#else:
		#	TYPE ERROR
	def sql_where(self,key,value):
		""" SQL WHERE LOGIC - TODO INCOMPLETE!"""
		self.mutate(key)
		if type(value) == dict:
			value_string = ', '.join([str(k) + ' = ' + str(v) for k,v in value.items()])
			self.mutate( value_string )
		elif type(value) in self.structure_type_checks:
			value_string = ', '.join([str(k) + ' = ' + str(v) for k,v in value])
			self.mutate( value_string )
		elif type(value) in self.value_type_checks:
			self.mutate(value)
		#else:
		#	TYPE ERROR
	def sql(self,text=None,**kwargs):
		""" Run input data through checks and perform necessary actions """
		if text is not None:
			if type(text) in self.value_type_checks:
				self.mutate(text)
			#else:
			#	TYPE ERROR
		else:
			for key, value in kwargs.items():
				key = key.upper()
				if '_' in key:
					key = key.split('_')[0] + ' ' + key.split('_')[1]
				if key == 'SELECT':
					self.sql_select(key,value)
				elif key == 'VALUES':
					self.sql_values(key,value)
				elif key == 'WHERE':
					self.sql_where(key,value)
				else:
					self.mutate(key)
					self.mutate(value)