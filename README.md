## Table of contents
* [General Info](#general-info)
* [Description](#description)
* [Technologies](#technologies)
* [Setup](#setup)
* [Execution](#execution)

## General Info
This project is Apache Airflow mini project

## Description
In this project, we will use Apache Airflow to create a data pipeline to extract online stock market data and deliver analytical results with Yahoo Finance as the data source. Yahoo Finance provides intra-day market price details down a one-minute interval.


## Technologies
Project is created as follows:
* Docker
* Python3.7+ (Libraries: yfinance,pandas)


## Setup

* Creating Custom Docker Image

To deploy Airflow with docker the best image to refer is puckel/docker-airflow. But this image can not be used as it is; due to few reasons. One reason is that it does not have all the packages installed that we are using in our project. If we need to change properties in airflow.config file, we have to pass them as environment variables. With a large number of variables this is not easy. So we will be writing a customized Dockerfile with the base image of puckel/docker-airflow. This image is going to be used in all our containers.


Following is our customized Dockerfile.

```
FROM puckel/docker-airflow:1.10.1

COPY airflow/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt


```

'docker-compose-LocalExecutor.yml' is used to pull the required images for executing our project

``` 
version: '3.7'
services:
    postgres:
        image: postgres:9.6
        environment:
            - POSTGRES_USER=airflow
            - POSTGRES_PASSWORD=airflow
            - POSTGRES_DB=airflow
```

Webserver

```
webserver:
        image: webserver:latest
        build:
          context: .
        restart: always
        depends_on:
            - postgres
        environment:
            - LOAD_EX=n
            - FERNET_KEY=46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=
            - EXECUTOR=Local
            - PYTHONPATH=/usr/local/airflow
        env_file:
          - env.list
        volumes:
            - ./airflow/dags:/usr/local/airflow/dags
            - ./scripts:/usr/local/airflow/scripts
            - ./tmp_data:/usr/local/tmp_data
            - ./finance_data:/usr/local/finance_data
        ports:
            - "8080:8080"
        command: webserver
        healthcheck:
            test: ["CMD-SHELL", "[ -f /usr/local/airflow/airflow-webserver.pid ]"]
            interval: 30s
            timeout: 30s
            retries: 3

```

* build context : point to the created custom Dockerfile. The correspond image is built when container is starting
* restart : re-deploy the container if it is stopped for any reason.
* depends_on : web server needs to communicate with meta db and message broker containers
* environment : These are the list environment variables requested by the base image puckel/docker-airflow. Keep them as it is. You are free to add more environment variables like ‘PYTHONPATH’ which are going to be used by your own program scripts.
* env_file: list of environment variables can be given using file
* volumes : dags and program scripts/datafolders can be mounted as volumes. This is more effective than copying files into the Docker image. Once the files are updated changes will be automatically deployed in the web server. No need to build the image and redeploy the container.
* ports : ports to be deployed on. web server is running on port 8080.
* command : airflow command to start the web server. This is requested by the base image puckel/docker-airflow. Do not modify it.
* healthcheck : test to check the health of the container


## Execution

Navigate to project folder and execute the following commands

Execute docker command to start a container

```
docker-compose docker-compose-LocalExecutor.yml up -d --build

```

Access airflow UI on http:localhost:8080 and trigger DAG


![Alt text](/Screenshots/airflowwebserver.PNG?raw=true "Airflow webserver")



Some important docker commands

Stop container

```
docker-compose -f docker-compose-LocalExecutor.yml down

```
View container

```
docker ps

```

Execute bash commands in container

```
docker exec -it <container-id> bash

```

Please refer document 'Airflow screenshots.docx' for detailed steps on airflow execution and logs.

