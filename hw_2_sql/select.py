from sqlite3 import Error

from connect import create_connection, database

def select_all_tasks_of_user(conn, user_id):
    """
    Retrieve all tasks for a specific user.
    :param conn: the Connection object
    :param user_id: the ID of the user
    :return: list of tasks for the user
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_all_tasks_with_status(conn, status):
    """
    Retrieve all tasks with a specific status.
    :param conn: the Connection object
    :param status: the status of the tasks to retrieve
    :return: list of tasks with the specified status
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks LEFT JOIN status ON tasks.status_id = status.id WHERE status.name=?", (status,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_users_without_task(conn):
    """
    Retrieve users who do not have any tasks.
    :param conn: the Connection object
    :return: list of users without tasks
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_uncompleted_tasks(conn):
    """
    Retrieve all tasks that are not completed.
    :param conn: the Connection object
    :return: list of uncompleted tasks
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE status_id NOT IN (SELECT id FROM status WHERE name='completed')")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_user_by_email(conn, email):
    """
    Retrieve user(s) by email address.
    :param conn: the Connection object
    :param email: the email address to search for
    :return: list of users matching the email
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email LIKE ?;", (email,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_number_of_tasks_for_each_status(conn):
    """
    Retrieve the number of tasks for each status.
    :param conn: the Connection object
    :return: list of tuples with status name and the count of tasks
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT status.name, COUNT(tasks.id) FROM tasks JOIN status ON tasks.status_id = status.id GROUP BY status.name")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_tasks_by_email_domain(conn):
    """
    Retrieve tasks assigned to users with a specific email domain.
    :param conn: the Connection object
    :param domain: the email domain to filter by (e.g., '@example.com')
    :return: list of tasks for users with the specified email domain
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT users.fullname, users.email FROM users LEFT JOIN tasks ON tasks.user_id = users.id WHERE users.email LIKE '%@example.com'")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def select_tasks_without_description(conn):
    """
    Retrieve tasks that have no description.
    :param conn: the Connection object
    :return: list of tasks without descriptions
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE tasks.description=''")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def get_users_with_tasks_in_progress(conn):
    """
    Retrieve users and their tasks that are in 'in progress' status.
    :param conn: the Connection object
    :return: list of tuples with user names and their tasks in 'in progress' status
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT users.fullname, tasks.title, status.name FROM users INNER JOIN tasks ON users.id = tasks.user_id INNER JOIN status ON tasks.status_id = status.id WHERE status.name = 'in progress'")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

def get_users_and_task_count(conn):
    """
    Retrieve users and the count of their tasks.
    :param conn: the Connection object
    :return: list of tuples with user names and the count of their tasks
    """
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT users.fullname, COUNT(tasks.id) FROM users LEFT JOIN tasks ON tasks.user_id = users.id GROUP BY users.fullname")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows

if __name__ == '__main__':
    with create_connection(database) as conn:
        print("All tasks of user with ID 24:")
        tasks_by_user = select_all_tasks_of_user(conn, 24)
        print(tasks_by_user)

        print("\nAll tasks with status 'new':")
        tasks_by_status = select_all_tasks_with_status(conn, 'new')
        print(tasks_by_status)

        print("\nList of users without any tasks:")
        users_without_task = select_users_without_task(conn)
        print(users_without_task)

        print("\nUncompleted tasks:")
        uncompleted_tasks = select_uncompleted_tasks(conn)
        print(uncompleted_tasks)

        print("\nUser with email 'leslie33@example.net':")
        user = select_user_by_email(conn, 'leslie33@example.net')
        print(user)

        print("\nNumber of tasks for each status:")
        number_of_tasks = select_number_of_tasks_for_each_status(conn)
        print(number_of_tasks)

        print("\nTasks assigned to users with email domain '@example.com':")
        tasks_by_domain = select_tasks_by_email_domain(conn)
        print(tasks_by_domain)

        print("\nTasks without description:")
        tasks_without_description = select_tasks_without_description(conn)
        print(tasks_without_description)

        print("\nUsers with tasks in progress:")
        users_in_progress = get_users_with_tasks_in_progress(conn)
        print(users_in_progress)

        print("\nUsers and their task counts:")
        users_and_task_count = get_users_and_task_count(conn)
        print(users_and_task_count)
