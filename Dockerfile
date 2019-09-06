FROM python

ENV DB_PORT 5432
ENV DB_TYPE postgresql
ENV DB_USER postgres
ENV DB_HOST host.docker.internal
ENV DB_PASSWORD nopassword
ENV DB_NAME modulelog
ENV DB_SCHEMA modulelog

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 8000

CMD ["gunicorn","server:connex_app","-b","0.0.0.0:8000"]
