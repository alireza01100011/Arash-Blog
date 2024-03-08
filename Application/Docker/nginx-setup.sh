#!/usr/bin/env bash
envsubst < /etc/nginx/org.nginx.conf.template > /etc/nginx/nginx.conf;
nginx -g 'daemon off;';