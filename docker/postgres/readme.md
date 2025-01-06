# eCommerce DB [Products]

## Running PostgreSQL & PgAdmin4 in docker
docker-compose up -d --build

After that create a new database in PgAdmin (Products database is already created)
Than copy dump file to the docker-compose.yml folder

### Copying a dump (backup file) to a container
docker cp ./<backup_file_name>.sql pg_db:/var/lib/postgresql/exports/<backup_file_name>.sql

docker cp ./test.sql pg_db:/var/lib/postgresql/exports/test.sql

### Database recovery 

docker exec -it pg_db sh
or
docker exec -it pg_db bash

pg_restore -U ${POSTGRES_USER} -d <your_db_name> -v /var/lib/postgresql/exports/<backup_file_name>.sql

pg_restore -U ${POSTGRES_USER} -d Products -v /var/lib/postgresql/exports/test.sql

exit

## Database backup
### Creating a dump file
docker exec -it pg_db sh

pg_dump -U ${POSTGRES_USER} -F c -b -v -f /var/lib/postgresql/exports/<backup_file_name>.sql <your_db_name>

exit

### Uploading backup to local machine

docker cp pg_db:/var/lib/postgresql/exports/<backup_file_name>.sql ./<backup_file_name>.sql

Now the backup file <backup_file_name>.sql will be in the current directory on your local machine. 
You can check it and use it as needed.
