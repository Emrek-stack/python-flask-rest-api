Development Setup

$ docker-compose build
$ docker-compose up

Run Flask Admin Commands
# go into the docker container and enter the virtualenv
$ make go_into_app
$ source /srv/maintenance.sh

# do stuff
$ flask resetdb

Add New Dependencies
# go into the docker container and enter the virtualenv
$ make go_into_app
$ source /srv/maintenance.sh

# install new pip modules in the venv here

# save them
$ pip freeze --local > requirements.txt