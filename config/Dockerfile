COPY ./nginx.conf /opt/nginx.conf.temp

CMD sed -e "s/ENV_PORT/$PORT/g" nginx.conf.temp > /tmp/nginx.conf && \
    nginx -c /tmp/nginx.conf -g "daemon off;"