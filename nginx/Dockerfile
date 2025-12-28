FROM nginx:1.29.4-trixie
RUN apt update && apt -y install certbot
RUN mkdir -p /etc/letsencrypt
COPY ./docker-entrypoint.d/90-copy-default-on-empty.sh /docker-entrypoint.d/
RUN mkdir -p /etc/nginx/defaults/
COPY ./default.conf /etc/nginx/defaults/default.conf
RUN rm /etc/nginx/conf.d/default.conf
