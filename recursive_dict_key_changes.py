def recursive_dict_pop(element,keys_tuple,new_key,start_counter=0):
	"""
	Check element for specified keys
	keys_tuple can be:
		- nested key address - a tuple of keys (key 1, key 2, key 3) with key 3 being the key that gets changed
		- a non-list/dict value to search for, recursively, throughout the nested dict keys
	------------------------------------------------------------------
	- If a key does not exist:
		- drop down into element level through recursion
		- check if it exists on later levels
	- if a key does exit:
		- pop it and assign back to element with key defined by new_key variable
	"""
	
	# -- if current element is a list, then we need to iterate over it and perform recursion again
	# the try except clause was to skip past an annoying TypeError when the recusion resets
	# videos have a title key, but the release title is also called title key
	# attempting to pop the release title key in the same way as here results in a TypeError
	# FIX: this was fixed by processing the release_title field first in the discogs project...
	
	if type(keys_tuple) is tuple:
		
		if type(element) is list:
				for list_item in element:
					for idx, key in enumerate(keys_tuple[start_counter:]):
						if key in list_item.keys():
							for b in recursive_dict_pop(list_item,keys_tuple,new_key,start_counter):
								yield True
						else:
							yield False

		# -- if at the last key address in keys_tuple, then pop the relevant dictionary element and return a True value
		elif len(keys_tuple[start_counter:]) == 1:
			old_key = keys_tuple[start_counter:][0]
			if type(element) is not list and old_key in element.keys():
				element[new_key] = element.pop(old_key)
				yield True
			else:
				yield False

		# -- else we need to recurse down further to find the relevant key name to swap
		# break fixes an AttributeError - 'title' name once again...!

		elif type(element) is not str:
			for idx, key in enumerate(keys_tuple[start_counter:]):
				if key in element.keys():
					start_counter+=1
					for b in recursive_dict_pop(element[key],keys_tuple,new_key,start_counter):
						yield True
				else:
					yield False
		else:
			yield False
	
	## ========= SINGLE KEY ADDRESS
	# - uses the same pattern as before, just without key_tuple fiddliness
	# --- if element is a list, iterate over the list and recursively search each list item's keys
	# --- if element is a dict and required key exists in element.keys(), pop the key into a new key name
	# --- if element is a dict and needed key not in element.keys(), drop down a level and keep searching
		
	elif type(keys_tuple) is not tuple and type(keys_tuple) is not dict:
		if type(element) is list:
			for list_item in element:
					if keys_tuple in list_item.keys():
						for b in recursive_dict_pop(list_item,keys_tuple,new_key,start_counter):
							yield True
					else:
						yield False
						
		elif type(element) is dict:
			if keys_tuple in element.keys():
				element[new_key] = element.pop(keys_tuple)
				yield True
			else:
				for key in element.keys():
					for b in recursive_dict_pop(element[key],keys_tuple,new_key,start_counter):
						yield True
		else:
			yield False