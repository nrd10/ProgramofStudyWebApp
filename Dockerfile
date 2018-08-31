FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/
RUN groupadd -g 1002 posuser && \
    useradd -r -u 1060403 -g posuser posuser
USER posuser
