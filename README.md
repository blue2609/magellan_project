- [Setup](#setup)
	- [Installing Python Package Dependencies](#installing-python-package-dependencies)
	- [Deploy PostgreSQL Databases](#deploy-postgresql-databases)
- [Running the Python Programs](#running-the-python-programs)
# Setup

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

Then, please run `sftp_sync.py` and specify the `<ping_sftp_interval>` which specifies the interval **(in seconds)** dictating the program `sftp_sync.py` to continuously ping the SFTP server for any:

- new **ASX300_NCS_CLS** files added to the SFTP server
- updated **ASX300_NCS_CLS** files in the SFTP server

by using this command from the root directory of the project:

```
python sftp_sync.py <ping_sftp_interval>
```




