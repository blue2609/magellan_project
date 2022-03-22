import pysftp
import psycopg2

class SftpServer:
	def __init__(
		self, 
		sftp_host: str, 
		sftp_username: str, 
		sftp_private_key: str,
		db_user: str, 
		db_password: str, 
		db_host: str,
		db_name: str
	):
		"""
		Initiate the state of the 'SftpServer' object 

		Parameters
		----------
		sftp_host : str
			The sftp_host name of the SFTP server
		
		sftp_username : str
			sftp_username to use to authenticate to the SFTP server
		
		sftp_private_key : str
			Path to the private key file to authenticate to the SFTP server

		db_user : str
			Username the program will use to access the database

		db_password : str
			Password the program will use to get access to the database

		db_host : str
			The host/IP address where the database resides

		db_name
			Name of the database which contains index files metadata 
		"""

		self.sftp_hostname = sftp_host
		self.sftp_username = sftp_username
		self.sftp_private_key = sftp_private_key
		self.db_user = db_user
		self.db_password = db_password
		self.db_host = db_host
		self.db_name = db_name
		self.__set_sftp_connection()
		self.__set_db_connection()
		self.__set_index_files()
	
	def __set_db_connection(self):
		"""
		Initiates the database connection
		"""
		self.db_conn = psycopg2.connect(
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            database=self.db_name
        )

	def __set_sftp_connection(self):
		"""
		Setup the SFTP connection to the SFTP server
		"""
		self.sftp= pysftp.Connection(
			host=self.sftp_hostname, 
			username=self.sftp_username, 
			private_key=self.sftp_private_key
		) 
	
	def __set_index_files(self):
		"""
		Set the list of index files attributes as object attribute 'index_files'
		"""

		self.index_files = []

		dir_structure = self.sftp.listdir_attr()
		for file_attr in dir_structure:
			if file_attr.filename.find('ASX300_NCS_CLS') > 0:
				self.index_files.append(file_attr)
	

	def __update_file_attrs_in_db(self):
		"""
		Update file attributes in database	
		"""
		update_file_attr_query = """
		UPDATE index_files SET (filesize, last_modified_time) = (%s, %s)
		WHERE 
			filename = %s AND
			(
				filesize != %s OR
				last_modified_time < %s
			)
		"""
		cur = self.db_conn.cursor()
		for file_attr in self.index_files:
			cur.execute(update_file_attr_query, (
				 	file_attr.st_size,
					file_attr.st_mtime,
					file_attr.filename,
					file_attr.st_size,
					file_attr.st_mtime
				)
			)
			self.db_conn.commit()
		cur.close()
	
	def __insert_new_file_attrs_in_db(self):
		"""
		Insert new file attribute records into the database
		"""

		insert_query = """
		INSERT INTO index_files (filename, filesize, last_modified_time) 
		SELECT %s AS filename, %s AS filesize, %s AS last_modified_time 
		WHERE NOT EXISTS (
			SELECT filename FROM index_files WHERE filename = %s
		);
		"""
		
		cur = self.db_conn.cursor()
		for file_attr in self.index_files:
			cur.execute(insert_query, (
					file_attr.filename,
					file_attr.st_size,
					file_attr.st_mtime,
					file_attr.filename
				)
			)
			self.db_conn.commit()
		cur.close()
	
	def sync_files_with_db(self):
		self.__update_file_attrs_in_db()
		self.__insert_new_file_attrs_in_db()
		

		
		



