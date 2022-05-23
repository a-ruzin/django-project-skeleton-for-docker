#!/bin/sh

PATH=/etc:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

PGPASSWORD=$POSTGRES_PASSWORD
export PGPASSWORD
dbUser=$POSTGRES_USER
database=$POSTGRES_DB

pathB=/var/lib/backup/data
mkdir -p $pathB

find $pathB -mtime +15 -delete
pg_dump -U $dbUser $database | gzip > $pathB/pgsql_$(date "+%Y-%m-%d").sql.gz


unset PGPASSWORD
