"""
Web scraping example for FFL.
scraping CBS Sports player pages for stats
in their completed games table
then combining into dataframes by position.
and then exporting them to csv files
"""
# from scrapeCbsFFL import scrape
from scrapeCbsFFLSoup import scrape
import csv
import pandas as pd

# list of players and the student owners
infname_join = 'scrapeCbsFFLPlayerStudentJoin.csv'

# list of players and their CBS FFL url
infname ='scrapeCbsFFLPlayers.csv'

# base url for CBS FFL players
base_url = 'https://www.cbssports.com/fantasy/football/players/'
current_week = 6

# init the dictionaries.  One for data frames, one for player-student LUT
dataframes_dict = {'QB':[],'RB':[], 'WR':[]}
player_student_dict = {}

# load player-student dictionary
with open(infname_join) as inf_join:
    csv_reader = csv.reader(inf_join)
    next(csv_reader)
    for row in csv_reader:
        player_name = row[0]
        student = row[1]
        player_student_dict[player_name] = student

# each player gets scraped
with open(infname) as inf:
    csv_reader = csv.reader(inf)
    next(csv_reader)
    for row in csv_reader:
        player_url_piece = row[0]
        player_name = row[1]
        position = row[2]

        print(f'{player_name}')

        url = base_url + player_url_piece
        foo = scrape(player_name, url, player_student_dict)
        dataframes_dict[position].append(foo)

# concatenate each of the tables by position then export to csv
for pos in dataframes_dict.keys():
    df = pd.concat(dataframes_dict[pos])
    export=df.to_csv(f'ffl_{pos}_week{current_week:02d}.csv', index=None, header=True)
