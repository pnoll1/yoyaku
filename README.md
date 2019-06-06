# Framework
  * Django v2
  * see requirements.txt for python dependencies

# Front End
  * Pure CSS/js
  * jinja2
  * Django Templates for admin interface
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

# Testing
  * possible
   * unit test

# Setup
 - setup venv
 - install dependencies
 - activate venv\
 - django-admin startproject “sitename”
 - fill in settings settings docs
 - python manage.py startapp “appname”
 - python manage.py runserver
 - python manage.py createsuperuser
  - needed to allow use of admin interface
 - install postgresql and postgis
 - create db named reservation
 - create postgis extension
 - setup user to match settings.py
 - import data using osm2pgsql, command in utils/overpass.sh
 - copy table to match django orm name CREATE TABLE home_planet_osm_point (like planet_osm_point including all);
 - good to go
