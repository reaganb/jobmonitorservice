FROM python:3.7-alpine

ADD . /app
WORKDIR /app
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install psycopg2-binary
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "server"]