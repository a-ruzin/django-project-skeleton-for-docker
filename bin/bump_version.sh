#!/bin/bash
part=$1
version=$([ -f VERSION ] && cat VERSION || echo "0.0.0")

# Split version into parts
IFS='.' read -r major minor patch <<< "$version"

# Increment the correct part
case $part in
  major)
    ((major++))
    minor=0
    patch=0
    ;;
  minor)
    ((minor++))
    patch=0
    ;;
  patch)
    ((patch++))
    ;;
  *)
    echo "Usage: $0 {major|minor|patch}"
    exit 1
    ;;
esac

# Update VERSION file
new_version="$major.$minor.$patch"
echo $new_version > VERSION
echo "Updated version to $new_version"
