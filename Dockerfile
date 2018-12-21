FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/
RUN groupadd posgroup
RUN useradd -m -G posgroup posuser
RUN mkdir /var/run/celery
RUN chown -R posuser:posgroup /var/run/celery/

USER posuser
