#!/bin/sh
# run vargrant up then vagrant ssh into box and run this script
python3 -m venv
. bin/activate
pip3 install -r requirements.txt
python manage.py createsuperuser --username admin #--password admin
su root
su postgres
psql -c "create database reservation"
psql -d reservation -c"CREATE EXTENSION postgis;"
psql -d reservation -c 'create extension "uuid-ossp";'
psql -d reservation -c "create user pat with password 'password';"
osm2pgsql --slim --username postgres --database reservation -C 300 nagoya_data.osm -S /vagrant/utils/restaurant.style
psql -d reservation -c "grant all on planet_osm_point to pat;"
psql -d reservation -c "ALTER TABLE planet_osm_point ADD uuid uuid default uuid_generate_v4();"
psql -d reservation -c "alter table planet_osm_point add city text default 'nagoya'"
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
