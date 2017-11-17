def check_and_create_folders( folder_var , create_flag = False):
	"""
	Function to check if a folder (or list of folders) exist on the base OS. If not, create the folder path.
	Folder_var must be a string or list input.
	Returns True if the fucntion did something, False and an error message if it did not.
	"""
	import os
	
	if type(folder_var) not in [list,str]:
		print('ERR: wrong input to check_and_create_folder() function. folder_var must be type str or list.')
		return False
		
	elif type(folder_var) is list and create_flag is True:

		if len(folder_var) > 1::
			for folder_path in folder_var:
				if not os.path.exists(folder_path):
					os.makedirs(folder_path)
			return True

		elif len(folder_var) == 1:
			if not os.path.exists(folder_var[0]):
				os.makedirs(folder_var)
			return True

		else:
			print('check_and_create_folders() function given a less than 1 length list of folder paths. check yourself before you wreck yourself.')
			return False
	
	elif type(folder_var) is str and create_flag is True:
		if not os.path.exists(folder_var):
        	os.makedirs(folder_var)
		return True
	
	else:
		print('No folders to create...')
		return False