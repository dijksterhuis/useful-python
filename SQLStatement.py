class SQLStatement:
	"""
	Object to handle bulding SQL queries from keyword argument/text inputs
	---------------------------------------
	Used like:
	>>> foo = SQLStatement()
	>>> foo.query()
	''
	>>> foo.sql(INSERT_INTO= 'site_visits', VALUES = (('visit_id',1), ('site_url', 'http://example.com')))
	>>> foo.query()
	'INSERT INTO site_visits (visit_id, site_url) VALUES (1, http://example.com)'
	>>> bar = SQLStatement('sql_query:')
	>>> bar.sql(text = 'SELECT "*"')
	>>> bar.sql(FROM = 'site_visits')
	>>> bar.sql(VALUES = {'visit_id' : 1 ,  'site_url' : 'http://example.com'})
	>>> bar.query()
	'sql_query: INSERT INTO site_visits (visit_id, site_url) VALUES (1, http://example.com)'
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
		if base_string == None:
			self.query_string = ''
		else:
			self.query_string = str(base_string) + ' '
	def mutate(self,string_value):
		self.query_string = self.query_string + '%s ' % string_value
		return True
	def query(self,string_value=None):
		return self.query_string[0:len(self.query_string) - 1 ]
	def forget(self,base_string=None):
		if base_string == None:
			self.query_string = ''
		else:
			self.query_string = str(base_string) + ' '
		return True
	def values_generator(self,values,index_selection):
		for key,value in values:
			output = (key,value)
			if type(output) == str and index_selection != 0:
				# Not quite working yet
				yield '"' + '%s' % output[index_selection] + '"'
			else:
				yield '%s' % output[index_selection]
	def sql(self,text=None,**kwargs):
		value_type_checks = [float,int,str,bool]
		structure_type_checks = [list,tuple]
		if text is not None:
			if type(text) in value_type_checks:
				self.mutate(text)
			#else:
			#	TYPE ERROR
		else:
			for key, value in kwargs.items():
				key = key.upper()
				if '_' in key:
					key = key.split('_')[0] + ' ' + key.split('_')[1]
				if key == 'SELECT':
					self.mutate(key)
					if type(value) in structure_type_checks:
						value_string = ', '.join(map(str,value))
						self.mutate(value_string)
					elif type(value) in value_type_checks:
						self.mutate(value)
					#else:
					#	TYPE ERROR
				elif key == 'VALUES':
					if type(value) == dict:
						name_string, value_string = tuple(', '.join([s for s in self.values_generator(value.items(),i)]) for i in range(0,2))
						self.mutate( '(%s)' % name_string + ' %s ' % key + '(%s)' % value_string)
					elif type(value) in structure_type_checks:
						name_string, value_string = tuple(', '.join([s for s in self.values_generator(value,i)]) for i in range(2))
						self.mutate('(%s)' % name_string + ' %s ' % key + '(%s)' % value_string)
					elif type(value) in value_type_checks:
						self.mutate(value)
					#else:
					#	TYPE ERROR
				else:
					self.mutate(key)
					self.mutate(value)