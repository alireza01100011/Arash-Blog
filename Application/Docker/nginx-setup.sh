#!/bin/sh


# Create Config File
envsubst "$(printf '${%s} ' $(env | cut -d'=' -f1))" < /etc/nginx/org.nginx.conf.template \
    > /etc/nginx/nginx.conf

# Start Nginx
nginx -g 'daemon off;'