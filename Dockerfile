FROM python:2

ARG APP_PATH=/hardware-checkout

WORKDIR $APP_PATH

ADD requirements.txt $APP_PATH
RUN pip install -r requirements.txt

ADD . $APP_PATH

EXPOSE 5000
CMD ["python", "runserver.py"]

