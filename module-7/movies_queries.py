"""
movies_queries.py

Module 7 – Query tables in the movies database.
"""

import mysql.connector
from mysql.connector import errorcode

# ---- DB CONFIG (same idea as your other movies assignments) ----
config = {
    "user": "root",          # change if your MySQL user is different
    "password": "sour",      # put YOUR MySQL password here
    "host": "127.0.0.1",
    "database": "movies",
    "raise_on_warnings": True
}


def main():
    try:
        # connect to the movies database
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        # 1) Select all fields from studio table
        print("-- DISPLAYING Studio RECORDS --")
        cursor.execute("SELECT studio_id, studio_name FROM studio;")
        studios = cursor.fetchall()
        for studio in studios:
            print(f"Studio ID:   {studio[0]}")
            print(f"Studio Name: {studio[1]}\n")

        # 2) Select all fields from genre table
        print("-- DISPLAYING Genre RECORDS --")
        cursor.execute("SELECT genre_id, genre_name FROM genre;")
        genres = cursor.fetchall()
        for genre in genres:
            print(f"Genre ID:   {genre[0]}")
            print(f"Genre Name: {genre[1]}\n")

        # 3) Movie names for movies with runtime less than 2 hours (< 120)
        print("-- DISPLAYING Short Film RECORDS --")
        cursor.execute(
            "SELECT film_name, film_runtime "
            "FROM film "
            "WHERE film_runtime < 120;"
        )
        short_films = cursor.fetchall()
        for film in short_films:
            print(f"Film Name: {film[0]}")
            print(f"Runtime:   {film[1]} minutes\n")

        # 4) Film names and directors grouped by director
        #    (ordering by director groups them visually)
        print("-- DISPLAYING Director RECORDS in Grouped Order --")
        cursor.execute(
            "SELECT film_name, film_director "
            "FROM film "
            "ORDER BY film_director, film_name;"
        )
        director_films = cursor.fetchall()
        for film in director_films:
            print(f"Director:  {film[1]}")
            print(f"Film Name: {film[0]}\n")

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
