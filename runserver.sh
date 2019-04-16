#!/bin/bash
while [ "1"=="1" ]
do
    gunicorn programofstudy.wsgi -b [::]:8000
    sleep 1
done
