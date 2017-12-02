from UnitTester import UnitTester

def demo():
    print("a = SQLBuilder()")
    a = SQLBuilder()
    print(a.query_get())
    
    print("a.sql( (('INSERT INTO','table'),) )")
    a.sql( (('INSERT INTO','table'),) )
    print(a.query_get())
    
    print("a.sql( {'VALUES':{'everything':'nothing','site':'example.com'}} )")
    a.sql( {'VALUES':{'everything':'nothing','site':'example.com'}} )
    print(a.query_get())
    
    print("    a.forget('SELECT (*)')")
    a.forget('SELECT (*)')
    print(a.query_get())
    
    print("a.sql( [['FROM','table_name']] )")
    a.sql( [['FROM','table_name']] )
    print(a.query_get())
    
    print("a.sql( {'WHERE':(('everything','nothing'),('site','example.com'))} )")
    a.sql( {'WHERE':(('everything','nothing'),('site','example.com'))} )
    print(a.query_pop())
    
    print("a.sql( (('INSERT INTO','table'),) )")
    a.sql( (('INSERT INTO','table'),) )
    print(a.query_get())
    
    print("a.sql( {'VALUES':{'everything':'nothing','site':'example.com'}} )")
    a.sql( {'VALUES':{'everything':'nothing','site':'example.com'}} )
    print(a.query_pop())
    
    print("print(a.query_pop())")
    print(a.query_get())
    
def unit_test():
    a, test_results = SQLBuilder(), UnitTester()
    
    # Test 1
    test_results.add_result( a.query_get() == '')
    
    # Test 2
    a.sql( (('INSERT INTO','table'),) )
    test_results.add_result(a.query_get() == 'INSERT INTO table ')
    
    # Test 3
    # --- Can fail due to dictionary ordering...!
    a.sql( {'VALUES':{'everything':'nothing','site':'example.com'}} )
    test_results.add_result(a.query_get() == 'INSERT INTO table (everything, site) VALUES (nothing, example.com) ' or a.query_get() == 'INSERT INTO table (site, everything) VALUES (example.com, nothing) ')
    
    # Test 4
    a.forget('SELECT (*)')
    test_results.add_result(a.query_get() == 'SELECT (*) ')
    
    # Test 5
    a.sql( [['FROM','table_name']] )
    test_results.add_result(a.query_get() == 'SELECT (*) FROM table_name ')
    
    # Test 6
    a.sql( {'WHERE':(('everything','nothing'),('site','example.com'))} )
    test_results.add_result(a.query_pop() == 'SELECT (*) FROM table_name WHERE everything = nothing, site = example.com ')
    
    # Test 7
    a.sql( (('INSERT INTO','table'),) )
    test_results.add_result(a.query_get() == 'INSERT INTO table ')
    
    # Test 8
    # --- Can fail due to dictionary ordering...!
    a.sql( {'VALUES':{'everything':'nothing','site':'example.com'}} )
    test_results.add_result(a.query_get() == 'INSERT INTO table (everything, site) VALUES (nothing, example.com) ' or a.query_get() == 'INSERT INTO table (site, everything) VALUES (example.com, nothing) ')
    a.query_pop()
    
    # Test 9
    test_results.add_result(a.query_get() == '')
    test_results.output()
    
class SQLBuilder:
    """
    ==================================================================
    Object to buld text SQL queries from packed argument/text inputs
    ==================================================================
    INFO
    ---------------------------------------
    SQLBuilder('starting string') is used to initialise the query string.
    - Takes either:
        - packed argument parameters
            - dictionary of commands e.g.:
                 - {'SELECT' : '(*)' , 'FROM' : 'table' }
            - nested tuples:
                - (('INSERT INTO','table'),)
                - (('INSERT INTO','table') , ('VALUES',(('everything','nothing'),('site','example.com'))))
            - or a combination of both:
                - (('INSERT INTO','table') , ('VALUES',{'everything':'nothing','site':'example.com' } ))
                - {'INSERT INTO':'table' , 'VALUES': (('everything','nothing'),('site','example.com' )) }
        - Text input using the text positional argument:
            - a.sql(text='SELECT (*)')
    - Strings can be built iteratively, or in one go.
    - a.query_get() returns the string for assignment without popping the query.
    - a.query_pop() pops the string for assignment.
    - a.delete(base_string=None) calls __init__.
    ---------------------------------------
    Usage
    ---------------------------------------
    >>> a = SQLBuilder()
    >>> a.sql( (('INSERT INTO','table'),) )
    >>> a.query_get()
    'INSERT INTO table '
    >>> a.sql( {'VALUES':{'everything':'nothing','site':'example.com'}} )
    >>> a.query_get()
    'INSERT INTO table (everything, site) VALUES (nothing, example.com) '
    >>> a.forget('SELECT (*)')
    >>> a.query_get()
    'SELECT (*) '
    >>> a.sql( [['FROM','table_name']] )
    >>> a.query_get()
    'SELECT (*) FROM table_name '
    >>> a.sql( {'WHERE':(('everything','nothing'),('site','example.com'))} )
    >>> a.query_get()
    'SELECT (*) FROM table_name WHERE everything = nothing, site = example.com '
    >>> a.sql( (('INSERT INTO','table'),) )
    >>> a.query_get()
    'INSERT INTO table '
    >>> a.sql( {'VALUES':{'everything':'nothing','site':'example.com'}} )
    >>> a.query_pop()
    'INSERT INTO table (everything, site) VALUES (nothing, example.com) '
    >>> print(a.query_get())
    ''
    ---------------------------------------
    TODO - more SQL operations
    TODO - Class methods -> missing, new (?)
    TODO - WHERE SQL logic for ANDs and ORs...?
    TODO DONE - Refactor code: move from **kwargs -> *args
    """
    
    def __init__(self,base_string=None):
        """ Initialise the string value """
        if base_string == None:
            self.query_string = str()
        else:
            self.query_string = str(base_string) + ' '
        self.structure_type_checks = set(i for i in [list,tuple,set])
        self.value_type_checks = set(i for i in [float,int,str,bool])
    def __mutate__(self,string_value):
        """ Mutate the current query string with a new string """
        self.query_string = self.query_string + '%s ' % string_value
        return True
    def __values_generator__(self,values,index_selection):
        """ Extract the right data from data types for VALUES sql command """
        if type(values) is dict:
            iterable = values.items()
        else:
            iterable = values
        for k,v in iterable:
            output = (k,v)
            if type(output) == str and index_selection != 0:
                # Not quite working yet
                yield '"' + '%s' % output[index_selection] + '"'
            else:
                yield '%s' % output[index_selection]
    def __sql_select__(self,k,v):
        """ SQL SELECT LOGIC """
        self.__mutate__(k)
        if type(v) in self.structure_type_checks:
            value_string = ', '.join(map(str,v))
            self.__mutate__(value_string)
        elif type(v) in self.value_type_checks:
            self.__mutate__(v)
        else:
            TypeError
    def __sql_values__(self,k,v):
        """ SQL VALUES LOGIC """
        if type(v) in self.value_type_checks:
            self.__mutate__(v)
        elif type(v) in self.structure_type_checks or type(v) is dict:
            name_string, value_string = tuple(', '.join([s for s in self.__values_generator__(v,i)]) for i in range(2))
            self.__mutate__('(%s)' % name_string + ' %s ' % k + '(%s)' % value_string)
        else:
            TypeError
    def __sql_where__(self,k,v):
        """ SQL WHERE LOGIC
        TODO - how to handle ANDS/ORS ?
        """
        self.__mutate__(k)
        if type(v) in self.value_type_checks:
            self.__mutate__(v)
        elif type(v) in self.structure_type_checks or type(v) is dict:
            value_string = ', '.join([str(x) + ' = ' + str(y) for x,y in v])
            self.__mutate__( value_string )
        else:
            TypeError
    def query_get(self):
        """ Return the query (slicing off extra whitespace (is it needed?!?!))
        - slicing chosen rather than stripping to allow further query clauses to be added
        """
        return self.query_string #[0:len(self.query_string) - 1 ]
    def query_pop(self):
        """ Return the query then 'pop' (forget) the value 
        TODO - this is hacky!
        """
        tmp = self.query_get()
        self.forget()
        return tmp
    def forget(self,base_string=None):
        """ Start over with a new string """
        self.__init__(base_string)
        #if base_string == None:
        #    self.query_string = ''
        #else:
        #    self.query_string = str(base_string) + ' '
        return True
    def sql(self,*args,text=None):
        """ Run input data through checks and perform necessary actions """
        if text is not None:
            if type(text) in self.value_type_checks:
                self.__mutate__(text)
            else:
                TypeError
        elif args:
            args = args[0] # *args puts everything into a single tuple element i.e. (args,)
            if type(args) in self.structure_type_checks:
                iterable = args
            elif type(args) is dict:
                iterable = args.items()
            else:
                TypeError
            for k, value in iterable:
                key = k.upper()
                if '_' in key:
                    key = '%s %s' % tuple('hello_world'.split('_'))
                if key == 'SELECT':
                    self.__sql_select__(key,value)
                elif key == 'VALUES':
                    self.__sql_values__(key,value)
                elif key == 'WHERE':
                    self.__sql_where__(key,value)
                else:
                    self.__mutate__(key)
                    self.__mutate__(value)
