FROM nginx:1.21-alpine
RUN apk add python3 python3-dev py3-pip build-base libressl-dev musl-dev libffi-dev rust openssl-dev cargo
RUN pip3 install pip --upgrade && pip3 install certbot-nginx
RUN mkdir /etc/letsencrypt
COPY ./docker-entrypoint.d/90-copy-default-on-empty.sh /docker-entrypoint.d/
RUN mkdir -p /etc/nginx/defaults/
COPY ./default.conf /etc/nginx/defaults/default.conf
