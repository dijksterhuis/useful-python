class Data_Output_Formatter:
	def __init__(self,data_output_type=None):
		if data_output_type == None: pass
		elif type(data_output_type) is not str: print('Type Error')
		elif data_output_type.upper() not in ['SQL','JSON','CSV','TSV']: print('Choice Error')
		else: self.output_type = data_output_type
		
	def sql_insert(self,sql_connection,table_name,column_names_and_values_dict):
		col_names = [key for key in column_names_and_values_dict.keys()]
		col_values = [column_names_and_values_dict[key] for key in col_names]
		
		col_string_fmt = ['{}' for i in range(len(column_names_and_values_dict))]
		sql_string = 'INSERT INTO {} (' + ', '.join(col_string_fmt).rstrip(',') +') VALUES (' + ', '.join(col_string_fmt).rstrip(',') +')'
		
		sql_command = sql_string.format(table_name,*col_names,*col_values )
		
		print(sql_command)