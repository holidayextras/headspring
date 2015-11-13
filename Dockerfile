FROM google/cloud-sdk

RUN apt-get update && apt-get install -y python-pip

RUN pip install google-api-python-client==1.4.2 flask tornado

ADD groducer/* /app/

CMD ["python", "/app/start.py"]
EXPOSE 8080

