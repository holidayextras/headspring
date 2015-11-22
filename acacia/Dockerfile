FROM google/cloud-sdk

RUN echo
RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y python-dev &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip

RUN groupadd -r acacia && useradd -r -g acacia acacia


COPY ship /bin/

ENTRYPOINT ["/bin/ship"]
CMD ["run"]

#COPY ship.d /etc/ship.d

#CMD ["/etc/ship.d/run"]
#COPY ship.d /etc/ship.d/
#RUN pip install google-api-python-client==1.4.2 flask tornado
#
#ADD headspring/* /app/
