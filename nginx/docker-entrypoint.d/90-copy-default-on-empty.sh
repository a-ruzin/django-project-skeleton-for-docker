#!/bin/sh

set -e

ME=$(basename $0)

copy_defaults() {
  local template_dir="${NGINX_DEFAULTS_DIR:-/etc/nginx/defaults}"
  local output_dir="${NGINX_CONF_D_DIR:-/etc/nginx/conf.d}"

  local template relative_path output_path subdir
  [ -d "$template_dir" ] || return 0
  if [ ! -w "$output_dir" ]; then
    echo >&3 "$ME: ERROR: $template_dir exists, but $output_dir is not writable"
    return 0
  fi
  find "$template_dir" -follow -type f -name "*.conf" -print | while read -r template; do
    relative_path="${template#$template_dir/}"
    output_path="$output_dir/${relative_path}"
    subdir=$(dirname "$relative_path")
    # create a subdirectory where the template file exists
    mkdir -p "$output_dir/$subdir"
    if [ ! -f "$output_path" -o "$template" -nt "$output_path" ]; then
      echo >&3 "$ME: Copying default $template to $output_path"
      envsubst '$PROJECT_DOMAIN $PROJECT_PORT' < "$template" > "$output_path"
    fi
  done
}

copy_defaults

exit 0
