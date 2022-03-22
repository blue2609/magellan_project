- [Setup](#setup)
	- [Setting up config files](#setting-up-config-files)
		- [Set up `config.ini`](#set-up-configini)
		- [Set Up Database Configuration](#set-up-database-configuration)
	- [Installing Python Package Dependencies](#installing-python-package-dependencies)
	- [Deploy PostgreSQL Databases](#deploy-postgresql-databases)
- [Running the Python Programs](#running-the-python-programs)
# Setup

This section assumes that you have:

- Python 3.8+ installed on your machine
- docker on your machine and docker daemon is already running

## Setting up config files

### Set up `config.ini`

Please create a `config.ini` file in the root directory of the project with this content

```
[SFTP_CONNECTION]
username = <sftp_username> 
hostname = <sftp_hostname>
ssh_key = <path_to_sftp_private_key>
```

where:

- `<sftp_username>` is the username the program will use to connect to the SFTP server
- `<sftp_hostname>` is the SFTP hostname the program should connect to
- `<ssh_key>` is the location to the private SSH Key file saved on your local machine which the program will use to authenticate itself against the SFTP server

### Set Up Database Configuration

As the program utilises 2 databases, there are 2 `.env` files user must configure as each file corresponds to configuration for each database.

For `sftp_db` database configuration, please go to `docker/sftp_db.env` and replace:
  - `<sftp_db_user>` with any username you want to use to connect to `sftp_db`
  - `<sftp_db_password>` with any password you want to use to connect to `sftp_db`

For `archive_db` database configuration, please go to `docker/archive_db.env` and replace:
  - `<archive_db_user>` with any username you want to use to connect to `archive_db`
  - `<archive_db_password>` with any password you want to use to connect to `archive_db`
  
##  Installing Python Package Dependencies

From the root directory of the project, run
```
pip install -r requirements.txt
```
## Deploy PostgreSQL Databases

First of all, please ensure that there'si no services running on your local machine's `localhost:5432`

From the root directory of the project, run 

```
docker-compose-up
```

This will deploy 2 databases `sftp_db` and `archive_db` in 2 separate containers.  Once the user receives a message saying 

```
LOG:  database system is ready to accept connections
```

for both `archive_db` and `sftp_db` in the terminal output after running the `compose` command, the databases are ready to use

# Running the Python Programs

From the root directory of the project, run

```
python data_archiver.py
```

which will keep listening and consume notifications generated by any **INSERT** or **UPDATE** operations on `index_files` table located in `sftp_db`

Then, please run `sftp_sync.py` and specify the `<ping_sftp_interval>` which tells the program to ping the SFTP server every `<ping_sftp_interval>` number of seconds. 

Everytime the program connects to the SFTP server, it will check the SFTP server for any:

- new **ASX300_NCS_CLS** files added to the SFTP server
- updated **ASX300_NCS_CLS** files in the SFTP server

by using this command from the root directory of the project:

```
python sftp_sync.py <ping_sftp_interval>
```

The program will now:
- Add the content of any new **ASX300_NCS_CLS** files in SFTP server to `archived_cls` table in `archive_db`.
- Check any modifications made to **ASX300_NCS_CLS** files in the SFTP server and update corresponding records in `archived_cls` table accordingly


