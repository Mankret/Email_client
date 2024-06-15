FROM nginx:latest as development_build

RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.backup
COPY ./config/nginx/conf.d/dev.conf /etc/nginx/conf.d