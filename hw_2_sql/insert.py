from sqlite3 import Error

from connect import create_connection, database

def add_task(conn, user_id, title, description, status_name):
    """
    Add a new task for a specific user.
    :param conn: the Connection object
    :param user_id: the ID of the user to whom the task is assigned
    :param title: the title of the new task
    :param description: the description of the new task
    :param status_name: the status of the new task (e.g., 'new', 'in progress')
    :return: None
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM status WHERE name=?", (status_name,))
        status_id = cur.fetchone()
        if status_id is None:
            print(f"Status '{status_name}' does not exist.")
            return
        
        status_id = status_id[0]
        
        cur.execute("""
            INSERT INTO tasks (user_id, title, description, status_id)
            VALUES (?, ?, ?, ?)
        """, (user_id, title, description, status_id))
        conn.commit()
        print(f"Task '{title}' added for user ID {user_id}.")
    except Error as e:
        print(e)
    finally:
        cur.close()

if __name__ == '__main__':
    with create_connection(database) as conn:
        add_task(conn, 3, 'Finish report', 'Complete the monthly financial report', 'new')
