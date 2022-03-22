# Setup

##  Installing Python Package Dependencies

From the root directory of the project, run
```
pip install -r requirements.txt
```

## SFTP application

### Deploy PostgreSQL DB

First of all, please ensure that there'si no services running on your local machine's `localhost:5432`

From the root directory of the project, run 

```
docker-compose-up
```

to get the postgres database container running. Once the user receives a message saying 

```
LOG:  database system is ready to accept connections
```

That means Postgres DB is ready to use
