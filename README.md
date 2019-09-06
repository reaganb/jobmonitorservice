# Job Monitor Service Project

## Using Flask, PostgreSQL, and Docker

Created a Containerized REST API server that can create, read, update, and delete job services in a local host database. 

### Prerequisites
1. Windows/Linux OS
2. Python 3
3. PostgreSQL database engine
4. Docker CE Engine
5. REST client

### Installation and Usage

#### Building the image and creating the container:

```Dockefile```
```
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
```
This is the ```Dockerfile``` that will be the basis of the image to be built. You can change the environmental variables depending on the database configuration your system have.

Take note of the value of the ```DB_HOST``` env variable. It has the domain name for the IP address of the host machine.

##### Build the image
```$ docker image build -t <image_name> .```
##### Create the container 
```$ docker container run -d -p 8000:8000 --name <container_name> <image_name>```

After this, it will automatically run the REST API server.
##### Test the connection
On the local machine

```$ curl localhost:8000/```


##### Manual setup for the database
Upon running the container, it will check if the database is present. 

If not, it will create that database and the schema. After that, you have to manually access the container to make some migrations to update the database table.


```
$ docker container exec -it <container_name> /bin/bash

root: /app # python manage.py migrate
root: /app # python manage.py upgrade
```

It will generate a new migration file to the ```migrations/versions``` folder and apply the changes to the database after.

#### Using the REST API server
To use the server, you must have a REST client to send requests from it.
One example of them is the POSTMAN app. You can download the app on https://www.getpostman.com/.

Another feature of the project is that the endpoints are not manually programmed. It uses ```Connexion```, a Python framework compatible with Flask that can automatically handle requests defined using OpenAPI(Swagger).

The endpoints and its specifications can be found on the ```swagger.yml``` file under the ```app``` module.

**Note**: for the ```PUT``` and ```DEL``` methods, it uses the column ``id`` as the parameter. Not the ```job_id``` column which is in uuid format.




