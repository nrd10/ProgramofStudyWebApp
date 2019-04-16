FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
RUN chmod 775 initserver.sh
RUN chmod 775 runserver.sh
RUN groupadd posgroup
RUN useradd -m -G posgroup posuser
RUN mkdir /var/run/celery
RUN chown -R posuser:posgroup /var/run/celery/
RUN chown -R posuser:posgroup /code/
RUN chown -R posuser /code
RUN chown posuser /code/initserver.sh
RUN chown posuser /code/runserver.sh
USER posuser

