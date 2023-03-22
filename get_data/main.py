import requests
from bs4 import BeautifulSoup
import psycopg2
from countryinfo import CountryInfo
import time
from dotenv import load_dotenv

load_dotenv()


class Population:
    def __init__(self, url, db_host, db_port, db_name, db_user, db_password):
        self.url = url
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def get_data(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', {'class': 'wikitable sortable'})
        rows = table.find_all('tr')

        count = 0

        for row in rows[3:]:
            try:
                cells = row.find_all('td')
                if len(cells) >= 2:

                    country = cells[0].text.strip()

                    population = cells[1].text
                    population_ = population.replace(',', '')
                    population_clear = int(float(population_))

                    region = self.check_region(country).region()
                    if region:
                        self.insert_data(country, population_clear, region)

                continue
            except Exception as e:
                cells = row.find_all('td')
                country = cells[0].text.strip()
                population = cells[1].text
                population_ = population.replace(',', '')
                population_clear = int(float(population_))
                self.insert_data(country, population_clear, 'Undefined')
                count += 1
                continue

        print('Parsing success!')

    def check_region(self, country):
        return CountryInfo(country)

    def insert_data(self, country, population, region):
        conn = psycopg2.connect(
            host=self.db_host,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

        cur = conn.cursor()
        table_create = ("""CREATE TABLE IF NOT EXISTS information (
        id SERIAL PRIMARY KEY,
        country VARCHAR(255) NOT NULL,
        population INTEGER,
        region VARCHAR(255)
         )""")

        cur.execute(table_create)
        cur.execute('INSERT INTO information (country, population, region) VALUES (%s, %s, %s)',
                    (country, population, region))

        conn.commit()
        conn.close()


if __name__ == '__main__':
    time.sleep(5)
    scraper = Population('https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population',
                         db_host='db',
                         db_port=5432,
                         db_name='population_db',
                         db_user='parser_user',
                         db_password='parser'
                         )
    scraper.get_data()
