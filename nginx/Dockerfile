FROM tutum/nginx

RUN rm /etc/nginx/sites-enabled/default

RUN mkdir -p /root/cannablr/cannablr/static
RUN mkdir -p /root/cannablr/cannablr/media
RUN chown -R www-data:www-data /root
ADD sites-enabled/ /etc/nginx/sites-enabled