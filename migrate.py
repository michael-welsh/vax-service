import logging
from mysql.connector import Error
from lib.dbconnection import get_db_connection
from google.cloud import datastore


logging.basicConfig(filename='logs/migration.log', level=logging.WARNING)


def migrate():

    print("Running migration")

    datastore_client = datastore.Client()

    try:
        db = get_db_connection()

        with db.connect() as conn:

            rv = conn.execute( "Select * from HK_SHOTS order by DATE" ).fetchall()

            result_id = 1

            for result in rv:

                # The kind for the new entity
                kind = "shot"
                # The name/ID for the new entity
                name = result_id
                task_key = datastore_client.key(kind, name)

                # Prepares the new entity
                task = datastore.Entity(key=task_key)
                task["date"] = result[0]
                task["first"] = result[2]
                task["first_daily"] = result[4]
                task["second"] = result[3]
                task["second_daily"] = result[5]
                task["total"] = result[1]
                task["total_daily"] = result[6]

                # Saves the entity
                datastore_client.put(task)

                result_id += 1

    except Error as error:
        #logging.error(error)
        print(error)

    return "success"


def get_back():

    print("pulling data")

    client = datastore.Client()

    key = client.key("Task", "shot")
    task = client.get(key)

    print(task)

def run_query(client):
    # [START datastore_run_query]
    query = client.query()
    results = list(query.fetch())
    # [END datastore_run_query]

    return results

if __name__ == '__main__':
    migrate()