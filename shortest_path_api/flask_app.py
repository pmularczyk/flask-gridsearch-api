# Standard library imports
import argparse
import re
import time
import uuid
from pathlib import Path

# Third party imports
from flask import Flask
from flask_restful import Api, Resource, reqparse
from sqlalchemy import create_engine

# Local application imports
from grid_search_app.grid_search import SearchSquareGrid

# Global variables
app = Flask(__name__)
api = Api(app)


def connect_to_database(path, name):
    
    db_location = Path(path)
    db_path = db_location.joinpath(name)

    db_connect = create_engine(
        f'sqlite:///{db_path}'
    )
    return db_connect

def get_timestamp():

    now = str(time.strftime('%Y-%m-%d %H:%M:%S'))

    return now

def validate_user_input(string, size):

    string = string.lower()
    regex = "[a-z]*-"

    user_input = [element.group() for element in re.finditer(regex, string)]
    validate = lambda string: string.endswith("-")

    result = list(map(validate, user_input))

    return len(result) == size - 1  # am Ende return message mit Error

class User(Resource):

    """ User class with methods POST and GET

    A user is able to input new data into the SearchSquareGrid
    which is going to find the shortest path between in this case
    mario, denoted as `m` and the princess, denoted as `p`
    
    The user has to provide a string that gets transformed into a grid later on
    the string has to look something like this:
    >>> oop-xox-mox where o's denote passable cells and x's denote walls

    The second argument a user has to pass is the size of the later grid which
    in this case would be 3

    As a user you and after giving correct arguments you immediately get
    your unique ID and result of the game. With your ID you can query the
    database later on with your get method
    """

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('data')
        parser.add_argument('size')
        args = parser.parse_args()

        if not validate_user_input(str(args['data']), int(args['size'])):
            raise Exception('Incorrect user input. Please provide input like omo-xxo-xpo')

        conn = db_connect.connect()

        id = str(uuid.uuid1().hex)

        grid = [element.replace('o', '-')
                for element in str(args['data']).split('-')]

        db_grid = ','.join(grid)

        lst_shortest_path = SearchSquareGrid(grid, int(args['size'])).get_path()
        str_shortest_path = re.sub("\'", "", str(lst_shortest_path))

        now = get_timestamp()

        # insert user data
        conn.execute('INSERT INTO "GridSearch" '
                     '(id, grid, time, result) '
                     f'VALUES ("{id}", "{db_grid}", "{now}", "{str_shortest_path}")')

        # select result for user
        response = conn.execute(
            f'select id, result from GridSearch where id = "{id}"')

        fetched = response.fetchall()

        # for first entry
        if len(fetched) == 1:

            id, result = fetched[0]
            entries = {'id': id, 'result': result}

        # for every other new entry
        else:

            entries = {'id': [element[0] for element in fetched],
                    'result': [element[1] for element in fetched]}

        return entries

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()

        id = args['id']

        conn = db_connect.connect()

        response = conn.execute(
            f'select result from GridSearch where id = "{id}"')

        entries = dict()
        for element in response.fetchall():

            userID, shortest_path = element
            entries['id'] = userID
            entries['result'] = shortest_path

        return entries


class Admin(Resource):

    """ The Admin class with method GET

    The Admin has the ability to get every entry of the database
    consisting of User IDs, Grids that where passed, the time when
    the User 'played the game' and his result
    """

    def get(self):

        conn = db_connect.connect()
        response = conn.execute(
            'select * from GridSearch')

        list_of_tuples = [elements for elements in response.fetchall()]
        entries = dict()
        for idx, element in enumerate(list_of_tuples):
            entries[str(idx + 1)] = {'id': element[0], 'grid': element[1],
                                     'time': element[2], 'result': element[3]}

    
        return entries


api.add_resource(User, '/users')
api.add_resource(Admin, '/admin')

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-p',
        '--path',
        type=str,
        required=True,
        help='The path where your database is located'
    )

    parser.add_argument(
        '-n',
        '--name',
        type=str,
        required=True,
        help='The name of your database'
    )

    options = parser.parse_args()

    if options.path is None:
        raise Exception('You have to provide a path where your database is located')

    if options.name is None:
        raise Exception('You have to provide the name of your database')

    db_connect = connect_to_database(options.path, options.name)
    
    app.run(port='5002')