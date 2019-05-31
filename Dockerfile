FROM python:3.6.3

ARG APP_PATH=/cog

WORKDIR $APP_PATH

ADD requirements.txt $APP_PATH
RUN pip install -r requirements.txt

ADD . $APP_PATH

EXPOSE 80
CMD ["python", "runserver.py"]

