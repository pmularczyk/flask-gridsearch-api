#!/bin/bash

path=~/databases

if [ ! -d $path ]
then
    echo "Directory ~/databases does not exist"
    mkdir $path
    
    sleep 5s
    cd shortest_path_api
    python3 database_creator.py --path=$path --name=$1.sqlite
    python3 flask_app.py --path=$path --name=$1.sqlite
else
    echo "Directory ~/databases exists"
    
    cd shortest_path_api
    python3 database_creator.py --path=$path --name=$1.sqlite
    python3 flask_app.py --path=$path --name=$1.sqlite
fi