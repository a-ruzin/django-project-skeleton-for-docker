#!/bin/sh

BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_DATE=$(git log -1 --format=%cd --date=iso)
VERSION=$(cat VERSION 2>/dev/null || echo "0.0.0")
echo "{\"version\": \"$VERSION\", \"branch\": \"$BRANCH\", \"commit\": \"$COMMIT_HASH\", \"date\": \"$COMMIT_DATE\"}"
