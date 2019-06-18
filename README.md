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
## Setup using current files
 - python3 -m venv env
 - . env/bin/activate
 - pip install -r requirements.txt
 - python manage.py createsuperuser
 - install postgresql and postgis
 - login to postgresql superuser, usually named postgres, may have to login to root then change to postgres if postgres has no password
 - psql -c "create database reservation;"
 - psql -d reservation
 - CREATE EXTENSION postgis;
 - create extension “uuid-ossp”; allows uuid_generate_v4();
 - create user pat with password 'password';
 - \q enter  to exit psql
 - install osm2pgsql
 - osm2pgsql --slim --username pat --database reservation nagoya_data.osm -S ./utils/restaurant.style
 - login to postgresql superuser
 - grant all on planet_osm_point to pat;
 - ALTER TABLE reservation ADD uuid uuid default uuid_generate_v4();
 - ./manage.py makemigrations
 - ./manage.py migrate
 - any issues delete everything in migrations and rerun migrations and migrate
 - ./manage.py runserver
 - website available at localhost:8000
 - localhost:8000/admin, login as superuser to manage db data graphically if needed
