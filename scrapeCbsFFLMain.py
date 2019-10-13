"""
Web scraping example from
https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
"""
# from scrapeCbsFFL import scrape
from scrapeCbsFFLSoup import scrape
import csv
import pandas as pd

infname ='scrapeCbsFFLPlayers.csv'

base_url = 'https://www.cbssports.com/fantasy/football/players/'
current_week = 6

dataframes_dict = {'QB':[],'RB':[], 'WR':[]}

with open(infname) as inf:
    csv_reader = csv.reader(inf)
    next(csv_reader)
    for row in csv_reader:
        player_url_piece = row[0]
        player_name = row[1]
        position = row[2]

        print(f'{player_name}, {position}')

        url = base_url + player_url_piece
        # print(url)
        foo = scrape(player_name, url, current_week)
        dataframes_dict[position].append(foo)

for pos in dataframes_dict.keys():
    df = pd.concat(dataframes_dict[pos])
    export=df.to_csv(f'ffl_{pos}_week{current_week:02d}.csv', index=None, header=True)
