# Image that you are going to inherite your docker file from 
#  Build images on top of images 
# Using the 3.7-alpine python image (light weight version of docker)
FROM python:3.7-alpine 

#  Maintainer line (Who is maintaining the project) optional 
MAINTAINER jean-marie 

#  Setup an environment variable 
# Reccommended to run pyhton in unbuffered mode in a docker container - prints outputs directly 

ENV PYTHONUNBUFFERED 1

# Install all the dependencies stored in the requirements.txt file 
# This line will copy the requrements from the root dir of the project to the docker image requirements file 
COPY ./requirements.txt /requirements.txt

# Take the copied requirements and install them to the image using pip 
RUN pip install -r /requirements.txt

# Create a directory in the docker image where the application and source code will be stored 
# 1. Create an empty folder named /app on the docker image 
# 2. On the docker image, switch to the /app as the default working directory where the application will run from 
# 3. Copy from the local machine the application to the /app folder created on the docker image 

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create a user that will run the application using docker 
# The -D specifies that the user being created will only be used to run applications/ processes in our image 
RUN adduser -D user 

# Switch to the created user in the docker image 
# Prevents the image from running the application using the root account 
USER user 