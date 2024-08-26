from sqlite3 import Error

from connect import create_connection, database

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)

if __name__ == '__main__':
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
     id integer PRIMARY KEY,
     fullname varchar(100) NOT NULL UNIQUE,
     email varchar(100) NOT NULL UNIQUE
    );
    """

    sql_create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
     id integer PRIMARY KEY,
     name varchar(50) NOT NULL UNIQUE
    );
    """

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
     id integer PRIMARY KEY,
     title varchar(100) NOT NULL,
     description text,
     status_id integer NOT NULL,
     user_id integer NOT NULL,
     FOREIGN KEY (status_id) REFERENCES status (id) ON DELETE CASCADE,
     FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """

    with create_connection(database) as conn:
        if conn is not None:
						# create users table
            create_table(conn, sql_create_users_table)
						# create status table
            create_table(conn, sql_create_status_table)
                        # create tasks table
            create_table(conn, sql_create_tasks_table)
        else:
            print("Error! cannot create the database connection.")
