FROM python:3.8-slim

RUN apt-get update && apt-get install -y supervisor wait-for-it

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

RUN python manage.py collectstatic --noinput

# RUN ./wait-for-it.sh postgres:5432
# RUN python manage.py migrate
# RUN python manage.py loaddata fixtures/initial_data.json

EXPOSE 8000 5432 6379

CMD [ "/usr/bin/supervisord", "-c", "supervisord.conf" ]