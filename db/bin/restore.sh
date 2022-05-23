#!/bin/sh

echo "
Restore should be done manually - no automation exists.

In common that is something like:
> psql -U \$POSTGRES_USER -d \$POSTGRES_DB -f backup.sql

Here is a couple of links to assist with:
 - https://stackoverflow.com/questions/2732474/restore-a-postgres-backup-file-using-the-command-line
 - https://www.postgresql.org/docs/13/backup-dump.html
"
