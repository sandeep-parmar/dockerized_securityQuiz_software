# dockerized_securityQuiz_software
This is a simple web app developed for fun for one of the hackathon project.
This web app is created using python flask web server and mysql as a database and bootstrap as a frontend technology

Recently as part of learning docker and containers , I have converted this web app to contianer images using docker compose utility

This is to understand how docker compose can be used to create a multi container application.
This application uses docker-compose tool to create 3 contianers

1. mysql for database
2. flask web server for rest apis
3. nginx server to host web pages

Tu run this web app, just clone this repo and perform below command

`docker-compose up --build`

docker-compose.yml looks like this

```
version: "3.8"
services:
   app:
      build: app/
      links:
         - mysql
      ports:
        - 5000:5000
   ##https://stavshamir.github.io/python/dockerizing-a-flask-mysql-app-with-docker-compose/ , https://medium.com/@shamir.stav_83310/dockerizing-a-flask-mysql-app-with-docker-compose-c4f51d20b40d
   mysql:
      image: mysql:5.7   # this is a base image
      ports:
         - 32000:3306    # map port 32000 of the host to the port 3306 of th4e mysql
      volumes:
        - ./db:/docker-entrypoint-initdb.d/:ro  #initialize the mysql schema from the sql file we have
        - todo-mysql-data:/var/lib/mysql
      environment:
         MYSQL_DATABASE: netbackup              # this is the database we want to create
         MYSQL_ROOT_PASSWORD: Gyp.s8m           # this the password we want to create for the user root of the mysql
   web:                                         #https://www.programials.com/docker-run-static-website
    image: nginx                                # use nginx as the base image
    volumes:
      - ./static:/usr/share/nginx/html          # mount volume from the current direcotory into the the public folder of the nginx so that any changes locally is reflected immeditely in the server
    container_name: illuminate-quiz             # use this as the container name
    restart: always                             # restart the server always
    ports:
      - 8081:80                                 # map port 8081 of the host to the port 80 of the container
volumes:
   todo-mysql-data:

```
