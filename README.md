Shortest Path API
=================

This package contains an API to find the shortest path between two cells in a sqare grid. 
It stores user input (ID, grid, time, result) in a database. The user gets back his result
i.e the shortest path between two cells for his grid.

**This was the original game setup:**
Mario and the princess are trapped in a square grid (N*N), Mario needs to reach the princess
with minimum number of steps (shortest paths), while avoiding any obstacles. Mario can
move UP, DOWN, LEFT and RIGHT and can’t go outside of the grid.
- Mario denoted by (m)
- Princess denoted by (p)
- Obstacle denoted by (x)
- Free cell denoted by (-)

If you want to use the API instead of just the SquareSearchGrid class you have to provide 
input that looks like this: 

1. data=oop-xox-mox,  where o's denote passable cells and x's denote walls

2. size=3, in this case because every row has 3 elements and the input consists of 3 rows

But first of all you have to create a database with the `database_creator.py`


## Database creator 

You call the database_creator.py like this
```
python3 database_creator.py --path=/home/user/databases --name=my_db.sqlite 
```

After calling the module you get a message prompted:
> Database created in: /home/user/databases/my_db.sqlite


```
usage: database_creator.py [-h] -p PATH -n NAME

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path where you want to store your database
  -n NAME, --name NAME  name of your database like my_db.sqlite
```

## Install postman [optional]

To use the API you have several options one of which is using postman GUI. This application let's you easily create GET, POST, PUT and DELETE requests (even more options).
It let's you specify parameters, headers, the request body and so on in an easy and reliable way.

```
snap install postman
``` 

## Start flask application

The next step after creating the database is starting the flask app like this:
With the parameters you can specify the database you want to connect to. In this case it is the database with
the table from the `database_creator`

```
python3 flask_app.py --path=/home/user/databases --name=my_db.sqlite 
```

Now the application is running in this location `http://127.0.0.1:5002/` and you can send POST and GET requests.

## Usage from command line

If you want to use curl there are some examples given below. 

### POST

```
curl -d "data=oop-xox-mox&size=3" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5002/users

curl -d '{"data":"oop-xox-mox", "size":"3"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5002/users
```

### GET

```
curl -i -H "Accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -X GET http://127.0.0.1:5002/admin

curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://127.0.0.1:5002/admin

```

### Requests library

Feel free to use python requests library as well, this would look something like this:
```
import json
import requests

url = http://127.0.0.1:5002/users
content = {'data':'oop-xox-mox', 'size':'3'}
headers = {
    'Content-Type': 'application/json'
}
try:
    response = requests.post(url,
                            headers=headers,
                            data=json.dumps(content))

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')

```

[flowchart](flowchart.png)
