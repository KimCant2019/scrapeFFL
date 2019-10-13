"""
Web scraping example using the Beautiful Soup
library.  Use the lxml parser.
Find the table with class "completed-games-table"
and then first read in all the headers
then go row by row and extract all the td data
making sure to remove * and convert - to 0
We skip the first row because it is a header row
and then we skip the final 2 rows b/c those are
projections and a footnotes item and we don't need
those.  # TODO: we could consider how to detect
non-integer values for column 1 and then ignore those
instead of hard-coding exclusion rows
"""
# import urllib.request
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape(player_name, url, player_student_dict):
    """
    player_name and url to scrape
    don't need num_week but leaving
    for legacy compatibility.
    could also add a table-class parm
    """
    TABLE_CLASS_TO_FIND = 'completed-games-table'
    # print(f'{player_name}, {url}')

    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    # print(soup.prettify())
    player_stat_table = soup.find('table', {'class':TABLE_CLASS_TO_FIND})
    # print(my_table)
    table_list = []
    table_rows = player_stat_table.find_all('tr')

# do table headers first
    header_row = table_rows[0].find_all('th')
    column_names = [header.text for header in header_row]
    column_names.insert(0,'Player')
    column_names.insert(1, 'Student')

# exclude the first TR (headers)
# and the final 2 TRs (projection and footnote)

    START_ROW = 1
    END_ROW = -2
    for tr in table_rows[START_ROW:END_ROW]:
        td = tr.find_all('td')
        row = [cell_data.text.replace('*','').strip() for cell_data in td]
        row = [0 if tr=='-' else tr for tr in row]
        row.insert(0,player_name)
        student_name = player_student_dict[player_name]
        row.insert(1,student_name)
        # if len(row)==0:
        #     continue
        table_list.append(row)
    result_dataframe = pd.DataFrame(table_list, columns=column_names)
    return result_dataframe

if __name__=='__main__':
    my_dict = {'Russell Wilson':'Brownie', 'Jared Goff':'Ninja'}

    url = 'https://www.cbssports.com/fantasy/football/players/1272242/russell-wilson'
    foo = scrape('Russell Wilson', url, my_dict)
    url = 'https://www.cbssports.com/fantasy/football/players/2061053/jared-goff'
    bar = scrape('Jared Goff', url, my_dict)
    print(pd.concat([foo,bar]))
