FROM python:3.8-slim

RUN apt-get update && apt-get install -y supervisor
# RUN mkdir -p /var/log/supervisor
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

# TODO migrate and create superuser

EXPOSE 8000 5432 6379

CMD [ "/usr/bin/supervisord", "-c", "supervisord.conf" ]