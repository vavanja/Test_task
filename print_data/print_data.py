import psycopg2
import time
from dotenv import load_dotenv

load_dotenv()


class CountryPopulation:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port

    def print_data(self):
        conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port
        )
        cur = conn.cursor()
        table_create = ("""CREATE TABLE IF NOT EXISTS information (
        id SERIAL PRIMARY KEY,
        country VARCHAR(255) NOT NULL,
        population INTEGER,
        region VARCHAR(255)
         )""")

        cur.execute(table_create)

        query = ("""
    SELECT
      region,
      SUM(population) AS total_population,
      MAX(country) FILTER (WHERE population = (SELECT MAX(population) FROM information WHERE region = info.region)) AS largest_country,
      MAX(population) FILTER (WHERE population = (SELECT MAX(population) FROM information WHERE region = info.region)) AS largest_country_population,
      MIN(country) FILTER (WHERE population = (SELECT MIN(population) FROM information WHERE region = info.region)) AS smallest_country,
      MIN(population) FILTER (WHERE population = (SELECT MIN(population) FROM information WHERE region = info.region)) AS smallest_country_population
    FROM
      information info
    GROUP BY
      region
""")

        cur.execute(query)
        rows = cur.fetchall()

        for row in rows:
            print('____________________________________________________________')
            print(f"Region: {row[0]}")
            print(f"Total population: {row[1]}")
            print(f"Biggest country: {row[2]}")
            print(f"Population of biggest country: {row[3]}")
            print(f"Smallest country: {row[4]}")
            print(f"Population of smallest country: {row[5]}")
        print('____________________________________________________________')
        cur.close()
        conn.close()


if __name__ == '__main__':
    time.sleep(5)
    scraper = CountryPopulation(
        db_host='db',
        db_port=5432,
        db_name='population_db',
        db_user='parser_user',
        db_password='parser'
    )
    scraper.print_data()
