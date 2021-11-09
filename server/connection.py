import mysql.connector

from syslogs import logs

def get_database():
    try:
        sql = mysql.connector.connect(
            host="localhost",
            username="root",
            password="om@123india",
            database="sahyata_db"
        )
    except Exception as e:
        logs.print_log(e, "error")
        sql = mysql.connector.connect(
            host="localhost",
            username="root",
            password="om@123india",
        )

        executor = sql.cursor()
        executor.execute("CREATE DATABASE sahyata_db")

        executor.execute(
            """
            CREATE TABLE students (
                ID          INT AUTO_INCREMENT PRIMARY KEY,
                name        VARCHAR(100),
                age         INTEGER,
                dob         DATE,
                class       INTEGER,
                traits      VARCHAR (255),
                soothers    VARCHAR (255),
                aggravators VARCHAR (255),
            )
            """
        )

    return sql
