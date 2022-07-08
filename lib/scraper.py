import datetime
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from mysql.connector import MySQLConnection, Error
from lib.dbconnection import get_db_connection
import sqlalchemy


chrome_options = Options()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--start-fullscreen')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

def scrape():
    print(os.environ.get('WEBDRIVER_PATH'))
    browser = webdriver.Chrome(options=chrome_options, service_log_path=os.environ.get('WEBDRIVER_LOG'), executable_path=os.environ.get('WEBDRIVER_PATH'))

    browser.get("https://www.news.gov.hk/eng/categories/covid19/index.html")
    soup = BeautifulSoup(browser.page_source, "html.parser")

    newsItems = soup.find_all("div", class_="news-summary")
    for summary in newsItems:
        if summary.text.find('doses of COVID-19 vaccines') != -1:
            x = 0
            shotsGiven = [0,0,0]
            print(summary.text)
            tokens = summary.text.split()
            for t in tokens:
                t = t.replace(',', '')
                if t.isnumeric():
                    shotsGiven[x] = int(t)
                    x += 1

            # Get the Date of the article
            summary_date_text = summary.previous_sibling.text
            summary_date = datetime.datetime.strptime(summary_date_text, "%B %d, %Y")

            try:
                db = get_db_connection()

                with db.connect() as conn:

                    sql = ("INSERT into HK_SHOTS (DATE, TOTAL, FIRST, SECOND) VALUES "
                           "(%(date)s, %(total)s, %(first)s, %(second)s)")
                    params = {
                        'date': summary_date,
                        'total': shotsGiven[0],
                        'first': shotsGiven[1],
                        'second': shotsGiven[2],
                    }
                    conn.execute(sql, params)

            except sqlalchemy.exc.IntegrityError:
                print('Duplicate records were found. These will be ignored. ')
            except Error as error:
                print(error)


    browser.quit()

