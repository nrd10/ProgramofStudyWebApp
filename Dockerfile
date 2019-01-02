FROM python:3.5
1;95;0cENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD . /code/
RUN groupadd posgroup
RUN useradd -m -G posgroup posuser
RUN mkdir /var/run/celery
RUN chown -R posuser:posgroup /var/run/celery/
RUN chown -R posuser:posgroup /code/
RUN chown -R posuser /code

USER posuser

