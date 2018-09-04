FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/celery
RUN touch /var/log/celery/programofstudy_beat.log
COPY programofstudy_celerybeat.conf /etc/supervisor/conf.d/programofstudy_celerybeat.conf
