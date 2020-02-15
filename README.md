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
Use docker-compose to run commands on the image that contains the django dependencies to create the project files needed for the application 
In the terminal run: 
1. `docker-compose run <name_of_the_service> <command_to_run_on_the_app>`
    ##### `sh` - shell 
    ##### `-c` - command being passed to the docker image 
    ##### `django-admin.py` - management command that comes with the installed version of django 
    ##### `startproject` - starts a django project named `app` with the default built in configuration in the current working directory
    e.g.: docker-compose run app sh -c "django-admin.py startproject app ."

2. Run the UNIT test configured in the application - `docker-compose run app sh -c "python manage.py test"`

#### Create a Core application that will maintain all shared modules

Run the command - `docker-compose run app sh -c "python manage.py startapp core"`
The core application will manage: 
- migrations 
- database 
    

### Continous integration 
- Travis-CI used on the github project 
- Automate tests and chechs when a new functionality is added and the application is pushed to GitHub
- Link you project to travis ci by signing up using your GitHub account on: `https://travis-ci.org/`
    - Authorize travis to access your projects 
    - If you don't have projects linked to travis, click on the plus button to then enable the project you wish to connect to travis 
- Create a travis CI configuration file. This tells travis what to do every time code is pushed to the repository 
    - Create the file in top root directory of the ptoject 


#### Creating additional applications 
When creating addional applications, use `--rm` to clean up your image 
Remove:
- the migration folder - managed in the core app  
- the admin.py file - managed in the core app 
- the tests.py - move them to a folder in called tests 
e.g.: ` docker-compose run --rm app sh -c "python manage.py startapp user"`

### Run the application by using: 
- command: `docker-compose up` 