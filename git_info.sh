#!/bin/sh

BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_DATE=$(git log -1 --format=%cd --date=iso)
echo "{\"branch\": \"$BRANCH\", \"commit\": \"$COMMIT_HASH\", \"date\": \"$COMMIT_DATE\"}"
