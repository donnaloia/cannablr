############################################################
# Dockerfile to build Ubuntu/Ansible/Django Image
# For deployment of Django skeleton project
############################################################

###########################################################
# How to run
# sudo docker build --no-cache -f Dockerfile .
# sudo docker run <containerid>
###########################################################


# Set the base image to Ansible
FROM ubuntu:16.10

# File Author / Maintainer
MAINTAINER Ben Donnaloia


###########################################################
# Install Python, Ansible and Related Depencies
###########################################################

RUN apt-get -y update && \
    apt-get install -y python-yaml python-jinja2 python-httplib2 python-keyczar python-paramiko python-setuptools python-pkg-resources git python-pip python-psycopg2 python-gdal
RUN mkdir /etc/ansible/
RUN echo '[local]\nlocalhost\n' > /etc/ansible/hosts
RUN mkdir /opt/ansible/
RUN git clone http://github.com/ansible/ansible.git /opt/ansible/ansible
WORKDIR /opt/ansible/ansible
RUN git submodule update --init
ENV PATH /opt/ansible/ansible/bin:/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin
ENV PYTHONPATH /opt/ansible/ansible/lib
ENV ANSIBLE_LIBRARY /opt/ansible/ansible/library
RUN apt-get update -y
RUN apt-get install python -y
RUN apt-get install python-dev -y
RUN apt-get install python-setuptools -y
RUN apt-get install python-pip



################## SETUP DIRECTORY STRUCTURE / COPY PROJ ######################


RUN mkdir -p /root/ansible
RUN mkdir -p /root/cannablr
RUN mkdir -p /root/nginxconf
RUN echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d
WORKDIR /root/cannablr/
COPY ./ ./
RUN chmod -R 777 ../


###########################################################
# Run the Playbook which will install Django
###########################################################

RUN ansible-playbook -c local ansible/playbooks/installdjango.yml


###########################################################
# Set environment variables
###########################################################

ENV PROJECTNAME benswebsite





###########################################################
# Start our Django project
###########################################################

WORKDIR /root/cannablr

EXPOSE 8000



