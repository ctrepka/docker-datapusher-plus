# docker-datapusher-plus

This repository makes use of [datHere's datapusher-plus](https://github.com/dathere/datapusher-plus) in a bare-bones Dockerfile to provide a basis for containerizing datapusher-plus.

`DataPusher+ is a fork of Datapusher that combines the speed and robustness of ckanext-xloader with the data type guessing of Datapusher.`

## Getting started with docker compose

To run a barebones install of datapusher-plus using docker compose, cd into the docker directory and run `docker-compose build` then `docker-compose up`. If you are utilizing v2 of docker compose, use `docker compose build` then `docker-compose up`.

The docker compose example in this repository utilizes mdillons postgis enabled postgresql image to provide a database for datapusher-plus to intialize and connect to. The scripts for database initialization and the Dockerfile used to build the database image can be found in ./docker/postgresql/docker-entrypoint-initdb.d and ./docker/postgresql respectively.

