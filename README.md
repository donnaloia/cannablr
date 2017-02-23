
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)
# Application Layout: 

 - 1 Authentication microservice written in Flask (custom token-based authentication)
 - 1 Redis service (where temp auth tokens are stored) 
 - 1 Nginx Load Balancer (serving the 2 parent services below)
 - 2 Parent server apps written in Django (Where most of the backend logic happens - pulls data from various API's into one place) 
 - 1 Postgres service 
 - 1 Messaging microservice written in Flask
 - 1 User/Profile microservice written in Flask

[![N|Solid](https://raw.github.com/donnaloia/cannablr/master/parentserver/housekeeping/Drawing.png)](https://raw.github.com/donnaloia/cannablr/master/web/housekeeping/Drawing.png)

# Build/CI/Deployment Layout:

When this project was live, the path to production looked like the following:
 - Each service has it's own Github Repository
 - When a pull request is initiated against any one of the repositories, a new build is triggered in CircleCI
 - If all tests pass, the pull request is merged into master
 - Github service hooks notify Docker Hub to build a new Docker image.
 - Web hooks running on EC2 detect when a new image is available on Docker Hub.  
 - If a new image is recognized, it is pulled down from Docker Hub and automatically deployed to the correct AWS instance via Docker.

Since this project is no longer live, I made some changes to the above steps outlined below:
 - The entire project (consisting of all the microservices and build/deploy infrastructure) is now contained within a single repository.
 - All the services above are mapped out in a docker-compose.yml with some small tweaks that enable a single-click production deploy.
 - Included is the Dockerrun.aws.json used to single-click deploy to AWS Elastic Beanstalk
 - Extensive use of environment variables and automation scripting to handle deployment from scratch (ie: deploying/configuring postgres with postGIS, populating database with location data, setting permissions, linking services, etc.)
 - Using Ansible in place of pip to install application dependencies
 - Static assetts were moved from an S3 bucket to the repository itself


# Open Source Tech
cannablr uses a number of open source projects to work properly
* [Flask] - a Python microframework!
* [Django] - a high level Python web framework
* [jQuery] - duh
* [Userena] - a Django library for custom user profiles/permissions
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [masonry.js] - a js library for vertically positioning UI elements
* [Docker] - containers for deploying applications


### Instructions

cannablr requires Docker to run.

Clone the repo and it's as simple as docker-compose up.

```sh
$ git clone https://github.com/donnaloia/cannablr.git
$ cd cannablr
$ docker-compose build
$ docker-compose up
```

For production environments...

```sh
$ git clone https://github.com/donnaloia/cannablr.git
$ cd cannablr
$ docker-compose build
$ docker-compose up
```

Now What?
```sh
$ docker-compose ps
$ docker inspect --format '{{ .NetworkSettings.IPAddress }}' parentserver
```
Curl or visit this ip address in your browser (port 8000) - the web app should be running and fully functional!

### Todos

 - Write MOAR Tests
 - The Flask Auth service is currently running using Flask's built in http server - This is obviously not production friendly


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [Django]: <https://www.djangoproject.com/>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [Flask]: <http://flask.pocoo.org/>
   [jQuery]: <http://jquery.com>
   [userena]: <https://github.com/bread-and-pepper/django-userena>
   [masonry.js]: <http://masonry.desandro.com/>
   [AngularJS]: <http://angularjs.org>
   [Docker]: <http://docker.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
