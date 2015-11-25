FROM acacia

RUN pip install google-api-python-client==1.4.2 flask tornado

ADD headspring/* /app/

COPY ship.d /etc/ship.d
EXPOSE 8080
