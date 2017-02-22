# Cannablr - a directory/social network for marijuana dispensaries to interact with customers.
This is a microservice-based project consisting: 
1 Auth Server written in Flask (custom token-based authentication)
1 Redis Server (where temp auth tokens are stored)
1 Nginx Load Balancer (serving the 2 parent services below)
2 Parent server apps written in Django (Where most of the backend logic happens - pulls data from various API's into one place)
1 Postgres instance
1 Messaging server

#CI/CD infastructure
This repository includes both the application code as well as the infastructure code
Deploying the included docker-compose will launch and link all of the contained services and handle failover.
Deploying via docker-compose and AWS CLI tools will succesfully deploy all contained services to AWS via Elastic Beanstalk (read instructions at the bottom for a more detailed explanation)


