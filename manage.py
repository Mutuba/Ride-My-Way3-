import os
import psycopg2


def create_tables():
    # Create users and requests tables
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            role BOOLEAN
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS rides(
            ride_id SERIAL PRIMARY KEY,
            ride_date TIMESTAMP NOT NULL,
            category VARCHAR(100) NOT NULL,
            pick_up VARCHAR(255) NOT NULL,
            drop_off VARCHAR(100) NOT NULL,
            date_time VARCHAR(100) NOT NULL,
            ride_status VARCHAR(100) NOT NULL,
            creator_id INT NOT NULL,
            FOREIGN KEY (
            creator_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS requests(
            request_id SERIAL PRIMARY KEY,
            request_date TIMESTAMP NOT NULL,
            request_description VARCHAR(255) NOT NULL,
            request_priority VARCHAR(100) NOT NULL,
            request_status VARCHAR(100) NOT NULL,
            requester_id INT NOT NULL,
            FOREIGN KEY (
            requester_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """
    )

    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"), database=os.getenv("DATABASE"),
            user=os.getenv("USER"), password=os.getenv("PASSWORD"))
        cur = conn.cursor()

        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    create_tables()
