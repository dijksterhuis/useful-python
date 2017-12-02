# useful-python
misc. useful python functions
----------------------------------------------------
### SQLStatement.py
Object to buld text SQL queries from packed argument/text inputs

#### INFO
- `SQLBuilder(base_string=None)` is used to initialise the query string.
- `a.sql(_*args,text=None)` takes either:
    - packed argument parameters
        - dictionary of commands e.g.:
             - `{'SELECT' : '(*)' , 'FROM' : 'table' }`
        - nested tuples:
            - `(('INSERT INTO','table'),)`
            - `(('INSERT INTO','table') , ('VALUES',(('everything','nothing'),('site','example.com'))))`
        - or a combination of both:
            - `(('INSERT INTO','table') , ('VALUES',{'everything':'nothing','site':'example.com' } ))`
            - `{'INSERT INTO':'table' , 'VALUES': (('everything','nothing'),('site','example.com' )) }`
    - Text input using the text positional argument:
        - `a.sql(text='SELECT (*)')`
- Strings can be built iteratively, or in one go.
- `a.query_get()` returns the string for assignment without popping the query.
- `a.query_pop()` pops the string for assignment.
- `a.forget(base_string=None)` calls `__init__` and reinitialises the whole object.

#### Example Usage
```python
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
```
#### TODOs
- more SQL operations
- Class methods -> `__missing__`, `__new__` (?)
- `WHERE` SQL logic for `AND`s and `OR`s...?
DONE - Refactor code: move from `**kwargs` -> `*args`
----------------------------------------------------
### UnitTester
Object to collect results of unit tests (boolean only for now) and then `print()` results to `stdout`
