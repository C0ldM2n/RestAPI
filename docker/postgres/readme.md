# eCommerce DB [Products]

## Running PostgreSQL & PgAdmin4 in docker
```shell
docker-compose up -d --build
```

After that create a new database in PgAdmin (Products database is already created)
Than copy dump file to the docker-compose.yml folder

### Copying a dump (backup file) to a container
```shell
docker cp ./<backup_file_name>.sql pg_db:/var/lib/postgresql/exports/<backup_file_name>.sql
```

### Database recovery
```shell
docker exec -it pg_db sh
```

```shell
pg_restore -U ${POSTGRES_USER} -d <your_db_name> -v /var/lib/postgresql/exports/<backup_file_name>.sql
exit
```

## Database backup
### Creating a dump file
```shell
docker exec -it pg_db sh
```

```shell
pg_dump -U ${POSTGRES_USER} -F c -b -v -f /var/lib/postgresql/exports/<backup_file_name>.sql <your_db_name>
exit
```

### Uploading backup to local machine
```shell
docker cp pg_db:/var/lib/postgresql/exports/<backup_file_name>.sql ./<backup_file_name>.sql
```

Now the backup file <backup_file_name>.sql will be in the current directory on your local machine. 
You can check it and use it as needed.
