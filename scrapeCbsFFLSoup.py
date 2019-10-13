"""
Web scraping example from
https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
"""
# import urllib.request
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape(player_name, url, num_week):
    # print(f'{player_name}, {url}')

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    # print(soup.prettify())
    my_table = soup.find('table', {'class':'completed-games-table'})
    # print(my_table)
    l = []
    table_rows = my_table.find_all('tr')

# do table headers first
    header_row = table_rows[0].find_all('th')
    column_names = [header.text for header in header_row]
    column_names.insert(0,'Player')

    for tr in table_rows[1:-2]:
        td = tr.find_all('td')
        row = [tr.text.replace('*','') for tr in td]
        row = [0 if tr=='-' else tr for tr in row]
        row.insert(0,player_name)
        # if len(row)==0:
        #     continue
        l.append(row)
    foo = pd.DataFrame(l, columns=column_names)
    return foo

if __name__=='__main__':
    url = 'https://www.cbssports.com/fantasy/football/players/1272242/russell-wilson'
    foo = scrape('Russell Wilson', url, 6)
    url = 'https://www.cbssports.com/fantasy/football/players/2061053/jared-goff'
    bar = scrape('Jared Goff', url, 6)
    print(pd.concat([foo,bar]))
