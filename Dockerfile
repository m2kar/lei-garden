FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip3 install requests
COPY ./app /app
