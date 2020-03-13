FROM python:3.6.3

ARG APP_PATH=/hardware-checkout

WORKDIR $APP_PATH

ADD requirements.txt $APP_PATH
RUN pip install -r requirements.txt

ADD . $APP_PATH

EXPOSE $FLASK_RUN_PORT
CMD ["python", "runserver.py"]
# CMD ["flask", "run"]
