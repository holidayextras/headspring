FROM google/cloud-sdk

RUN echo
RUN apk update && apk upgrade

RUN apk add --upgrade alpine-sdk python-dev py-pip

RUN addgroup -S acacia && adduser -S acacia acacia

COPY ship env_to_config_override.py /bin/

ENTRYPOINT ["/bin/ship"]
CMD ["run"]

#COPY ship.d /etc/ship.d

#CMD ["/etc/ship.d/run"]
#COPY ship.d /etc/ship.d/
#RUN pip install google-api-python-client==1.4.2 flask tornado
#
#ADD headspring/* /app/
