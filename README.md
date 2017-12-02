# useful-python
misc. useful python functions

## SQLStatement.py
Object to buld text SQL queries from packed argument/text inputs

### INFO
- `a = SQLBuilder(base_string=None)` is used to initialise the query string.
- `a.sql(*args,text=None)` takes either:
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

### Example Usage
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
### TODOs
- more SQL operations
- Class methods -> `__missing__`, `__new__` (?)
- `WHERE` SQL logic for `AND`s and `OR`s...?
- DONE - Refactor code: move from `**kwargs` -> `*args`

## UnitTester
- Object to collect results of unit tests (boolean only for now) and then `print()` results to `stdout`
Usage:
```python
>>> from UnitTester import UnitTester
>>> test_results = UnitTester()
>>> # Test 1 = True
>>> test_results.add_result( True )
>>> # Test 2 = False
>>> test_results.add_result( False )
>>> # Test 2 = True
>>> test_results.add_result( True )
>>> test_results.output()

2 of 3 tests successful

Some tests failed, here are the results:

    test 1 status: OK
    test 2 status: FAIL
    test 3 status: OK

```

## check_and_create_folders
Arguments:
```python
check_and_create_folders( folder_var , create_flag = False)
```
- Function to check if a folder (or list of folders) exist on the base OS. If not, create the folder path.
- Folder_var must be a string or list input.
- Returns True if the function did something, False and an error message if it did not.
- `create_flag = True` allows the function to create folders. Any other value will not.

## recursive_dict_key_changes
Arguments:
```python
recursive_dict_pop(element,keys_tuple,new_key,start_counter=0)
```
Generator function tp check element for specified keys and then pop their value back into the same object with a new key address
- keys_tuple can be:
	- nested key address - a tuple of keys (key 1, key 2, key 3) with key 3 being the key that gets changed
	- a non-list/dict value to search for, recursively, throughout the nested dict keys
- If a key does not exist:
	- drop down into element level through recursion
	- check if it exists on later levels
- if a key does exit:
	- pop it and assign back to element with key defined by new_key variable
