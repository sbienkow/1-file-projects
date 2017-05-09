"""Scrape data from imdb and store it in database."""
import sys
import os
from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup as BS
from time import sleep
import sqlite3


def main():
    website = "http://www.imdb.com/chart/top"
    try:
        content = urlopen(website)
    except URLError as err:
        print(err)
    else:
        soup = BS(content.read(), "lxml")
        content.close()
        titleColumn = soup.find('tbody').findAll('td', class_='titleColumn')
        moviesIds = [movie.find('a')['href'].split('/')[2] for movie in titleColumn]
        movie_credits_site = "http://www.imdb.com/title/{}/fullcredits"
        con = sqlite3.connect('movies.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS movies(title text, cast blob)')
        for movieId in moviesIds:
            content = urlopen(movie_credits_site.format(movieId))
            msoup = BS(content.read(), "lxml")
            content.close()
            title = msoup.find('h3', itemprop='name').find('a', itemprop='url').string
            cur.execute('SELECT rowid FROM movies WHERE title = ?', (title,))
            if cur.fetchone() is None:
                cast_list = msoup.find('table', class_='cast_list')
                cast_span = cast_list.findAll('span',
                                              class_='itemprop',
                                              itemprop='name')
                cast_name = [span.string for span in cast_span]
                cur.execute('INSERT INTO movies VALUES (?, ?)',
                            (title, repr(cast_name)))  # TODO Change repr to something safer

            sleep(1)
        con.commit()
        con.close()
    return 0


def show_database():
    con = sqlite3.connect('movies.db')
    cur = con.cursor()
    movies = cur.execute('SELECT * FROM movies').fetchall()
    for movie in movies:
        print(movie[0], eval(movie[1]))
        break
    con.close()


def delete_database():
    os.remove('movies.db')  # Can throw FileNotFoundError if database don't exist


def export_database(filename):
    with open(filename, 'w') as f:
        con = sqlite3.connect('movies.db')
        cur = con.cursor()
        movies = cur.execute('SELECT * FROM movies').fetchall()
        for movie in movies:
            f.write('{}: {}\n'.format(movie[0], eval(movie[1])))
        con.close()


if __name__ == '__main__':
    sys.exit(main())

if False:  # Used for interactive session
    main()
    show_database()
    delete_database()
    export_database('movies.txt')
