from modules.cls_file_schema import ClsFileSchema
import pandas as pd
from dotenv import load_dotenv
import psycopg2
import numpy as np
import os
import logging
import pysftp

class ClsFile:
	def __init__(self, file_name: str, sftp: pysftp.Connection):
		"""
		Initiate the state of 'ClsFile' object si it will have connection to the pysftp server and 'archive_db' database

		Parameters
		----------
		file_name : str
			file name of the index file this object is associated with
		
		sftp : pysftp.Connection
			The sftp connection to the server
		"""
		self.file_name = file_name
		self.sftp = sftp
		self.__set_df()
		self.__validate_df()
		self.__set_conn_to_archive_db()
		self.__set_col_names()
		self.__set_sql_col_names()
	
	def __set_df(self):
		self.df = pd.read_csv(
			self.sftp.open(self.file_name), 
			skipfooter=1, 
			sep='\t',
			dtype=str,
			engine='python'
		)
		self.df['id'] = self.df['EFFECTIVE DATE'] + self.df['TICKER']

	def __validate_df(self):
		cls_file_schema = ClsFileSchema()	
		schema = cls_file_schema.get_schema()
		self.errors = schema.validate(self.df, columns=schema.get_column_names())
	
	def log_errors(self, event_name: str):
		logging.warning(f"Error detected in file {self.file_name}")
		
		if event_name == 'new_file_added':
			logging.warning(f"Abort insert operation to 'archive_db'")
			for error in self.errors:
				logging.warning(error)
				
		elif event_name == 'file_updated':
			logging.warning(f"Abort update operation to 'archive_db'")
			for error in self.errors:
				logging.warning(error)

	def __set_conn_to_archive_db(self):
		load_dotenv(dotenv_path="./docker/archive_db.env", override=True)
		db_user = os.getenv('POSTGRES_USER')
		db_password = os.getenv('POSTGRES_PASSWORD')

		self.archive_db_conn = psycopg2.connect(
			user=db_user,
			password=db_password,
			host='localhost',
			database='archive_db',
			port=5433
		)

	def __set_col_names(self):
		self.col_names = list(self.df.columns)
	
	def __set_sql_col_names(self):
		self.sql_col_names = [
			col_name.lower().strip().replace(' ','_') 
			for col_name in self.col_names
		]

	def sync_records_with_archive_db(self):
		"""
		Sync records in the file with its existing records in 'archive_db'
		"""
		print(f"Updating {self.file_name} records in archive_db")
		cur = self.archive_db_conn.cursor()

		sql_col_names_str = ','.join(self.sql_col_names)
		placeholder_str = ','.join(['%s'] * len(self.sql_col_names))

		update_query_str = f"""
		UPDATE archived_cls SET ({sql_col_names_str}) = ({placeholder_str})
		WHERE id = %s
		"""
		for _, row in self.df.iterrows():
			cur.execute(update_query_str, np.append(row.values, row['id']))
			self.archive_db_conn.commit()
		
		cur.close()

	
	def insert_records_to_archive_db(self):
		"""
		Insert new records in the file into 'archive_db'
		"""
	
		print(f"Inserting {self.file_name} records into archive_db")
		cur = self.archive_db_conn.cursor()

		sql_col_names_str = ','.join(self.sql_col_names)
		placeholder_str = ','.join(['%s'] * len(self.sql_col_names))

		insert_query_str = f"""
		INSERT INTO archived_cls ({sql_col_names_str})
		VALUES
		({placeholder_str})
		"""

		# print(insert_query_str)
		for _, row in self.df.iterrows():
			cur.execute(insert_query_str, row.values)
			self.archive_db_conn.commit()

		cur.close()
	

		
		
		