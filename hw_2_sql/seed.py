from sqlite3 import Error
from faker import Faker
import random

from connect import create_connection, database

def create_user(conn, user):
    """
    Create a new user into the users table
    :param conn:
    :param user:
    :return: user id
    """
    sql = '''
    INSERT INTO users(fullname,email) VALUES(?,?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, user)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid

def create_status(conn, status):
    """
    Create a new status
    :param conn:
    :param status:
    :return:
    """

    sql = '''
    INSERT INTO status(name) VALUES(?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, status)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = '''
    INSERT INTO tasks(title,description,status_id,user_id) VALUES(?,?,?,?);
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, task)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return cur.lastrowid

if __name__ == '__main__':
    fake = Faker()
    users_number = 25
    with create_connection(database) as conn:
                        # status
        status = [('new',), ('in progress',), ('completed',)]
                        # create status
        status_id = []
        status_id.append(create_status(conn, status[0]))
        status_id.append(create_status(conn, status[1]))
        status_id.append(create_status(conn, status[2]))

        for i in range(users_number):
                        # users
            user = (fake.name(), fake.email())
                        # create users
            user_id = create_user(conn, user)
            
            tasks_number = random.randint(0, 3)
            
            for j in range(tasks_number):
                        # tasks
                task = (fake.sentence(nb_words=3, variable_nb_words=True), fake.text(), random.choice(status_id), user_id)
                        # create tasks
                create_task(conn, task)

