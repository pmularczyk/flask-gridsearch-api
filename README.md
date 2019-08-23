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


## Usage of grid_search.py

You can use the grid_search.py module within your Python environment. The user input has to look like this:

```
data = ['p--','x-x','x-m']
size = 3
```

if you want to use a larger grid for example `size = 4` you have to add an element to each string and add an additional fourth string of length 4 like this `['-p--','xx-x','xx--', 'm--x']`

Inside a python environment or the REPL
```{python}
from shortest_path_api.gridsearch_app.grid_search import SearchSquareGrid

data = ['p--','x-x','x-m']
size = 3
grid = SearchSquareGrid(data, size)

grid.breadth_first_search()
[1] [(2, 2), (2, 1), (1, 1), (0, 1), (0, 0)]

grid.get_path()
[2] ['Left', 'Up', 'Up', 'Left']
```
## Usage of API

If you want to use the API instead of just the SquareSearchGrid class you have to provide input that looks like this: 

- **start** denoted by (m)
- **end** denoted by (p)
- **obstacle** denoted by (x)
- **passable** denoted by (o)

**example input**

1. data=oop-xox-mox,  where o's denote passable cells and x's denote walls

2. size=3, in this case because every row has 3 elements and the input consists of 3 rows

## Start the application

You can start the application with the `init-script.sh`. First of all go to the respective directory `shortest_path_api`. The user has to input a databasename as argument.
```
./init-script.sh <database-name>
```

The startup script creates a databases directory if it does not exist and creates a database with user defined name.
After calling the module you get a message prompted:
> Database created in: /home/user/databases/mydb.sqlite

after the database is created the script starts the flask app.
Now the application is running in this location `http://127.0.0.1:5002/` and you can send POST and GET requests.


## Usage from command line

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
## Requests library

If you want to use curl there are some examples given below. Feel free to use python requests library as well, this would look something like this:
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

## Install postman [optional]

To use the API you have several options one of which is using postman GUI. This application let's you easily create GET, POST, PUT and DELETE requests (even more options).
It let's you specify parameters, headers, the request body and so on in an easy and reliable way.

```
snap install postman
``` 

![flowchart.png]("flowchart.png")