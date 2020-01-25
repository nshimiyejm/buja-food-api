# buja-food-api
Recipt app api source code learning with Django 

#### Commands
Build the image: `docker build .`

- Create a docker-compose configuration for the project in the root dir 
    - It enables to run the docker image from the project location (working dir)
    - Manage the different services that makeup the project 
        - e.g.: python service that we run or 
                database service that we run 

Build the composed services: `docker-compose build`