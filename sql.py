# This file is responsible for creating the table and creating the database
import sqlite3

try:
    # Connect to sqlite
    connection = sqlite3.connect("student.db")

    # Create a cursor object to insert records, create table, and retrieve records
    cursor = connection.cursor()

    # Create a table
    table_info = """
    CREATE TABLE IF NOT EXISTS STUDENT(
        NAME VARCHAR(25),
        CLASS VARCHAR(25),
        SECTION VARCHAR(25),
        MARKS INT
    );
    """
    cursor.execute(table_info)

    # Insert some records
    students = [
        ('Adil', 'Data Science', 'A', 90),
        ('Rauf', 'Data Science', 'B', 100),
        ('Zain', 'Data Science', 'A', 86),
        ('Zulqarnain', 'DEVOPS', 'A', 50),
        ('Ittefaq', 'DEVOPS', 'A', 35)
    ]
    cursor.executemany('''INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?)''', students)

    # Display all records
    print("The Inserted Records are:")
    cursor.execute('''SELECT * FROM STUDENT''')
    for row in cursor.fetchall():
        print(row)

    # Commit and close the connection
    connection.commit()

except sqlite3.Error as error:
    print(f"Error while working with SQLite: {error}")

finally:
    if connection:
        connection.close()
