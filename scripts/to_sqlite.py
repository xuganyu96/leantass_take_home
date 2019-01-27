#   a number of methods for creating and filling a local sqlite3 database

import sqlite3 as sql
from sqlite3 import Error

#   Create a database at a specified path
def create_conn(path):
    #   Given the desired path to the to-be-created database
    #   and return the cursor object of the connection

    conn = sql.connect(path)
    return(conn.cursor(), conn)

def create_table(table_name, cur):
    #   cases and blocks both use the same sets of column names
    #   which will be fixed for simplier code here

    #   Given a string that is the name of the table and a cursor object
    #   execute a query that create the table with the specified table name
    #   and blocks/cases columns with appropriate attributes

    query = '''
    CREATE TABLE IF NOT EXISTS table_name (
        end_dttm DATETIME,
        room TEXT,
        start_dttm DATETIME,
        id INTEGER PRIMARY KEY
    );
    '''

    #   replace the question mark with the name of the table
    #   then execute this query
    query = query.replace('table_name', table_name)
    cur.execute(query)

def add_values(table_name, values, cur):
    #   Given a cursor object, add values to the specified table
    #   values will be a list of tuples

    try:
        #   Construct the skeleton query
        insert_query = '''
            INSERT INTO table
                (end_dttm, room, start_dttm, id) VALUES
                (?, ?, ?, ?)
        '''
        #   Fill in the table name
        insert_query = insert_query.replace('table', table_name)
        #   Execute the query
        cur.executemany(insert_query, values)
    except Error as E:
        print(E)

def parse_csv(file_path):
    #   Given the path to a csv file that is either a block or a case csv
    #   return a list of tuples of values

    #   read in the file indicated by the file_path
    #   split the read parts by line breaker
    #   then remove the header and the last empty row because the document ends with
    #   a line breaker
    rows = open(file_path).read().split('\n')[1:-1]

    #   Use list interpretation to convert a list of rows into a list of
    #   tuples of values
    values = [tuple(row.split(',')) for row in rows]

    # print(values)
    #   return the values
    return values
