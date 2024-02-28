#!/bin/sh


envsubst "$(printf '${%s} ' $(env | cut -d'=' -f1))" < /etc/nginx/org.nginx.conf.template \
    > /etc/nginx/nginx.conf

nginx -g 'daemon off;'