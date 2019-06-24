# Framework
  * Django v2
  * see requirements.txt for python dependencies

# Front End
  * Pure CSS/js
  * jinja2
  * Django Templates for admin interface
  * SASS
  * JS libs
    * leaflet
    * markercluster
  * possible
    * Webpack or parcel? build pipelines
    * NPM

# Backend
  * postgresql v10
  * osm2pgsql
     * use script in /util to download osm data into postgres
  * possible
    * mapbox search api
    * google places api

# Testing
  * unittest
## Testing setup
  * db user may need superuser in db to create objects for test
  * development server is running
  * ./manage.py test

# Setup
 - setup venv
   - python3 -m venv env
 - activate venv
   - . env/bin/activate
 - install dependencies
   - pip install -r requirements.txt
 - django-admin startproject “sitename”
 - fill in settings settings docs
 - python manage.py startapp “appname”
 - python manage.py createsuperuser
   - needed to allow use of admin interface
 - install postgresql and postgis
 - create db named reservation
 - create postgis extension
 - setup user to match settings.py
 - import data using osm2pgsql, command in utils/overpass.sh
 - run migrations to setup reservation table
 - python manage.py runserver
 - good to go
## Setup using Vagrant
 - vagrant up
 - vagrant ssh
 - run setupssh.sh
 - site available at localhost:8000
