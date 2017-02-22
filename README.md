
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)
# Application Layout: 

 - 1 Authentication microservice written in Flask (custom token-based authentication)
 - 1 Redis service (where temp auth tokens are stored) 
 - 1 Nginx Load Balancer (serving the 2 parent services below)
  - 2 Parent server apps written in Django (Where most of the backend logic happens - pulls data from various API's into one place) 
 - 1 Postgres service 
 - 1 Messaging microservice written in Flask
 - 1 User/Profile microservice written in Flask

# DevOpsy Stuff:
 - All the services above are mapped out in a docker-compose.yml with some small tweaks that enable a single-click production deploy.
 -  Included is the Dockerrun.aws.json used to single-click deploy to AWS Elastic Beanstalk
 - Extensive use of environment variables and automation scripting to handle deployment from scratch (ie: deploying/configuring postgres with postGIS, populating database with location data, linking services, etc) 
 - A pull request results in a new build being triggered on circleCI, if the build is greenlit, the pull request is merged into master and a new image is pushed to Dockerhub.
 - When this project was live in AWS, I had webhooks that would trigger an automated deploy to AWS when a new image was detected on Dockerhub

# Open Source Tech
cannablr uses a number of open source projects to work properly
* [Flask] - a Python microframework!
* [Django] - a high level Python web framework
* [jQuery] - duh
* [Userena] - a Django library for custom user profiles/permissions
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [masonry.js] - a js library for vertically positioning UI elements


### Instructions

Cannablr requires Docker to run.

Clone the repo and let Docker work its magic.

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
$ docker inspect <containername>
```
Curl or visit this ip address in your browser - the web app should be running and fully functional!

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
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
