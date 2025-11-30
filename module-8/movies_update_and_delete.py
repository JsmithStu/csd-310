"""
movies_update_and_delete.py

Module 8 – Update and Delete records in the movies database.
"""

import mysql.connector
from mysql.connector import errorcode

# ---- DB CONFIG (change user/password if your setup is different) ----
config = {
    "user": "root",              # or movies_user, etc.
    "password": "sour", # <-- put YOUR MySQL password here
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}


def show_films(cursor, title):
    """
    Display film name, director, genre, and studio
    using INNER JOINs on genre and studio.
    """
    query = """
        SELECT
            film_name    AS Name,
            film_director AS Director,
            genre_name   AS Genre,
            studio_name  AS Studio
        FROM film
        INNER JOIN genre
            ON film.genre_id = genre.genre_id
        INNER JOIN studio
            ON film.studio_id = studio.studio_id
        ORDER BY film_name;
    """

    cursor.execute(query)
    films = cursor.fetchall()

    print(f"\n-- {title} --")
    for film in films:
        print(f"Film Name: {film[0]}")
        print(f"Director:  {film[1]}")
        print(f"Genre:     {film[2]}")
        print(f"Studio:    {film[3]}\n")


def main():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        # 1. Display original films
        show_films(cursor, "DISPLAYING FILMS")

        # 2. INSERT a new film (pick a film, use existing studio/genre)
        #    Adjust studio_name / genre_name here if your DB uses different names.
        insert_sql = """
            INSERT INTO film
                (film_name, film_releaseDate, film_runtime,
                 film_director, studio_id, genre_id)
            VALUES
                (%s, %s, %s, %s,
                 (SELECT studio_id FROM studio WHERE studio_name = %s),
                 (SELECT genre_id FROM genre WHERE genre_name = %s));
        """

        new_film = (
            "Inception",        # film_name
            2010,               # film_releaseDate
            148,                # film_runtime
            "Christopher Nolan",# film_director
            "20th Century Fox", # studio_name in your studio table
            "SciFi"             # genre_name in your genre table
        )

        cursor.execute(insert_sql, new_film)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

        # 3. UPDATE Alien to be a Horror film
        update_sql = """
            UPDATE film
            SET genre_id = (
                SELECT genre_id
                FROM genre
                WHERE genre_name = 'Horror'
            )
            WHERE film_name = 'Alien';
        """

        cursor.execute(update_sql)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

        # 4. DELETE Gladiator
        delete_sql = "DELETE FROM film WHERE film_name = 'Gladiator';"
        cursor.execute(delete_sql)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

        cursor.close()
        db.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print(err)


if __name__ == "__main__":
    main()
