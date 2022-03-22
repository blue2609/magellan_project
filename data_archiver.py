from modules.sftp_server import SftpServer 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import configparser
from dotenv import load_dotenv
from psycopg2._psycopg import connection
from modules.cls_file import ClsFile
import pysftp
import json
import logging
import os


def db_listen(sftp_db_conn: connection, sftp_conn: pysftp.Connection):
	#set to autocommit
	sftp_db_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = sftp_db_conn.cursor()
	cur.execute("LISTEN new_file_added;")
	cur.execute("LISTEN file_updated;")
	
	while True:
		#get the message 
		sftp_db_conn.poll()
		
		while sftp_db_conn.notifies:
			notification =  sftp_db_conn.notifies.pop()  #pop notification from list
			payload_dict = json.loads(notification.payload)
			filename = payload_dict.get('filename')

			cls_file = ClsFile(filename, sftp_conn)
			if notification.channel == 'new_file_added':
				print(f'\n\nnew file "{filename}" is detected in the SFTP server')
				if cls_file.errors:
					cls_file.log_errors()
					continue

				cls_file.insert_records_to_archive_db()

			if notification.channel == 'file_updated':
				print(f'file "{filename}" has been updated in SFTP server')
				if cls_file.errors:
					cls_file.log_errors(notification.channel)
					continue
				cls_file.sync_records_with_archive_db()

def init_config():
	config = configparser.ConfigParser()
	config.read("config.ini")
	return config

def main():
	logging.basicConfig(level=logging.WARNING)
	config = init_config()
	
	# get sftp config
	sftp_hostname = config['SFTP_CONNECTION']['hostname']
	sftp_username = config['SFTP_CONNECTION']['username']
	sftp_ssh_key_path = config['SFTP_CONNECTION']['ssh_key']

	# obtain sftp_db config
	load_dotenv(dotenv_path="./docker/sftp_db.env")
	db_user = os.getenv('POSTGRES_USER')
	db_password = os.getenv('POSTGRES_PASSWORD')

	# initialise sftp server connection object and its db connection
	sftp_server = SftpServer(
		sftp_host=sftp_hostname, 
		sftp_username=sftp_username,
		sftp_private_key=sftp_ssh_key_path,
		db_user=db_user,
		db_password=db_password,
		db_host="localhost",
		db_name="sftp_db"
	)

	#listen to channel 
	db_listen(sftp_server.db_conn, sftp_server.sftp)

	

if __name__ == "__main__":
	main()