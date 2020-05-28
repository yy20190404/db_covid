FROM alpine

COPY ./supervisord.conf /etc/

CMD sed -e "s/ENV_PORT/$PORT/g" nginx.conf.temp > /tmp/nginx.conf && \
    supervisord -c /etc/supervisord.conf