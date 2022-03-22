from modules.sftp_server import SftpServer 
import configparser
from dotenv import load_dotenv
import os
import argparse
import time


def init_config():
	config = configparser.ConfigParser()
	config.read("config.ini")
	return config

def init_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('ping_sftp_interval', help='Tells the program to ping the SFTP server every x no. of seconds', type=int)
	return parser.parse_args()

def main():
	config = init_config()
	args = init_args()
	sftp_hostname = config['SFTP_CONNECTION']['hostname']
	sftp_username = config['SFTP_CONNECTION']['username']
	sftp_ssh_key_path = config['SFTP_CONNECTION']['ssh_key']

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

	while True:
		try:
			time.sleep(args.ping_sftp_interval)
			sftp_server.sync_files_with_db()
		except KeyboardInterrupt:
			print("Keyboard interrupt is detected, closing connection to SFTP and sftp_db")
			sftp_server.sftp.close()
			sftp_server.db_conn.close()
			exit(1)

if __name__ == "__main__":
	main()