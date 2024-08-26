from sqlite3 import Error

from connect import create_connection, database

def update_task_status(conn, status, task_id):
    """
    update status of a task
    :param conn:
    :param parameters:
    :return:
    """
    sql = '''
    UPDATE tasks
    SET status_id = ?
    WHERE id = ?
    '''

    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM status WHERE name=?", (status,))
        status_id = cur.fetchone()
        if status_id is None:
            print(f"Status '{status}' does not exist.")
            return
        
        parameters = (status_id[0], task_id)

        cur.execute(sql, parameters)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

def update_user_name(conn, parameters):
    """
    update fullname of user
    :param conn:
    :param parameters:
    :return:
    """
    sql = '''
    UPDATE users
    SET fullname = ?
    WHERE id = ?
    '''

    cur = conn.cursor()
    try:
        cur.execute(sql, parameters)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()

if __name__ == '__main__':
    with create_connection(database) as conn:
        update_task_status(conn, 'in progress', 1)
        update_user_name(conn, ('Natalie L', 1))
