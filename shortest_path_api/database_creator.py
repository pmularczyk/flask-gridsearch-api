# Standard library imports
import argparse
from pathlib import Path

# Third party imports
from sqlalchemy import create_engine

"""  database_creator.py 

    Creates a database with four columns 
    - id VARCHAR NOT NULL
    - grid VARCHAR
    - time VARCHAR
    - result VARCHAR
    - PRIMARY KEY (id)

    Parameters:
    -----------
    path : string
        the location on your local filesystem where you want to store the database

    name : string
        the name of the database e.g. my_db.sqlite

    Returns:
    --------
    prompt : stdout
        e.g. Database created in: /home/user/databases/my_db.sqlite


    Examples:
    ---------
    >>> python3 database_creator.py --path=/home/user/databases --name=my_db.sqlite
    """

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-p',
        '--path',
        type=str,
        required=True,
        help='path where you want to store your database'
    )

    parser.add_argument(
        '-n',
        '--name',
        type=str,
        required=True,
        help='name of your database like my_db.sqlite'
    )

    options = parser.parse_args()

    if options.path is None:
        raise Exception('You have to provide a path where you want to store your database in your local filesystem')

    if options.name is None:
        raise Exception('You have to provide a name for your database like my_db.sqlite')
    
    db_location = Path(options.path)
    db_path = db_location.joinpath(options.name)

    db_uri = f"sqlite:///{db_path}"

    engine = create_engine(db_uri)

    # create table
    engine.execute('CREATE TABLE "GridSearch" ('
                'id VARCHAR NOT NULL,'
                'grid VARCHAR,'
                'time VARCHAR,'
                'result VARCHAR,'
                'PRIMARY KEY (id));')

    print(f"Database created in: {db_path}")