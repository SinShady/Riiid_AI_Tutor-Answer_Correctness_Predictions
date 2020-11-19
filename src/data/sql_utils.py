import psycopg2
import pandas as pd
import os

DBNAME = "riiid-education"

def create_database_and_tables():
    create_database()
    create_tables()
    print("Successfully created database and all tables")
    print()


def create_database():
    """
    This function assumes that you have an existing database called `postgres`
    without any username/password required to access it.  Then it creates a new
    database called `opportunity_youth`
    """
    # Depending on your local settings, you may need to specify a user and password, e.g.
    # conn = psycopg2.connect(dbname="postgres", user="postgres", password="password")
    conn = psycopg2.connect(dbname="postgres")
    conn.autocommit = True  # it seems this mode is needed to make a db
    conn.set_isolation_level(0)  # also this for dropping db

    # un-comment this line if you already have a database called
    # `opportunity_youth` and you want to drop it
    # execute_sql_script(conn, "01_drop_old_database.sql")
    execute_sql_script(conn, "02_create_new_database.sql")

    conn.close()


def create_tables():
    """
    Composite function that creates all relevant tables in the database
    This creates empty tables with the appropriate schema, then the data
    transfer is performed in the `copy_csv_files` function
    """
    # Depending on your local settings, you may need to specify a user and password, e.g.
    # conn = psycopg2.connect(dbname=DBNAME, user="postgres", password="password")
    conn = psycopg2.connect(dbname=DBNAME)

    create_train_table(conn)
    create_questions_table(conn)
    create_lectures_table(conn)
    create_example_test_table(conn)
    create_example_test_table(conn)

    conn.close()


def create_train_table(conn):
    """
    Create a table for the train data
    """
    execute_sql_script(conn, "03_train_table.sql")


def create_questions_table(conn):
    """
    Create a table for the questions data
    """
    execute_sql_script(conn, "04_create_questions_table.sql")


def create_lectures_table(conn):
    """
    Create a table for the lectures data
    """
    execute_sql_script(conn, "05_create_lectures_table.sql")


def create_example_test_table(conn):
    """
    Create a table for the example_test data
    """
    execute_sql_script(conn, "06_create_example_test_table.sql")


def create_example_sample_submission_table(conn):
    """
    Create a table for the census tract to example_sample_submission data
    """
    execute_sql_script(conn, "07_create_example_sample_submission_table.sql")


def copy_csv_files(data_files_dict):
    """
    Composite function that copies all CSV files into the database
    """
    # Depending on your local settings, you may need to specify a user and password, e.g.
    # conn = psycopg2.connect(dbname=DBNAME, user="postgres", password="password")
    conn = psycopg2.connect(dbname=DBNAME)

    for name, files in data_files_dict.items():
        csv_file = files[0]
        # skip the header; this info is already in the table schema
        next(csv_file)
        if name == "train":
            copy_csv_to_train_table(conn, csv_file)
        elif name == "questions":
            copy_csv_to_questions_table(conn, csv_file)
        elif name == "lectures":
            copy_csv_to_lectures_table(conn, csv_file)
        elif name == "example_test":
            copy_csv_to_example_test_table(conn, csv_file)
        elif name == "example_sample_submission":
            copy_csv_to_example_sample_submission_table(conn, csv_file)

        print(f"""Successfully loaded CSV file into `{name}` table
        """)

    conn.close()


def copy_csv_to_train_table(conn, csv_file):
    """
    Copy the CSV contents of the train data into the table
    """
    COPY_TRAIN = "08_copy_train_to_table.psql"
    copy_expert_psql_script(conn, COPY_TRAIN, csv_file)


def copy_csv_to_questions_table(conn, csv_file):
    """
    Copy the txt contents of the questions data into the table
    """
    COPY_QUESTIONS = "09_copy_questions_to_table.psql"
    copy_expert_psql_script(conn, COPY_QUESTIONS, csv_file)


def copy_csv_to_lectures_table(conn, csv_file):
    """
    Copy the csv contents of the lectures data into the table
    """
    COPY_LECTURES = "10_copy_lectures_to_table.psql"
    copy_expert_psql_script(conn, COPY_LECTURES, csv_file)


def copy_csv_to_example_test_table(conn, csv_file):
    """
    Copy the csv contents of the example test data into the table
    """
    COPY_EXAMPLE_TEST = "11_copy_example_test_to_table.psql"
    copy_expert_psql_script(conn, COPY_EXAMPLE_TEST, csv_file)


def copy_csv_to_example_sample_submission_table(conn, csv_file):
    """
    Copy the csv contents of the census tract to example sample submission data
    into the table
    """
    COPY_EXAMPLE_SAMPLE_SUBMISSION = "12_copy_ct_example_sample_submissionk_to_table.psql"
    copy_expert_psql_script(conn, COPY_EXAMPLE_SAMPLE_SUBMISSION, csv_file)


def execute_sql_script(conn, script_filename):
    """
    Given a DB connection and a file path to a SQL script, open up the SQL
    script and execute it
    """
    file_contents = open_sql_script(script_filename)
    cursor = conn.cursor()
    cursor.execute(file_contents)
    conn.commit()


def open_sql_script(script_filename):
    """
    Given a file path, open the file and return its contents
    We assume that the file path is always inside the sql directory
    """
    dir = os.path.dirname(__file__)
    relative_filename = os.path.join(dir, 'sql', script_filename)

    file_obj = open(relative_filename, 'r')
    file_contents = file_obj.read()
    file_obj.close()

    return file_contents


def copy_expert_psql_script(conn, script_filename, csv_file):
    """
    Given a DB connection and a file path to a PSQL script, open up the PSQL
    script and use it to run copy_expert
    """
    file_contents = open_sql_script(script_filename)
    cursor = conn.cursor()
    cursor.copy_expert(file_contents, csv_file)
    conn.commit()
