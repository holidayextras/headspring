FROM python:2

RUN pip install google-api-python-client==1.4.2 flask tornado

ADD groducer/* /app/

CMD ["python", "/app/start.py"]
EXPOSE 8080

