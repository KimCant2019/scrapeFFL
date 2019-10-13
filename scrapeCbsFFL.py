"""
Web scraping example from
https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
"""
# import urllib.request
import requests
import lxml.html as lh
import pandas as pd

def scrape(player_name, url, num_week):
    # print(f'{player_name}, {url}')

    page = requests.get(url)
    doc = lh.fromstring(page.content)
    tr_elements=doc.xpath('//tr')

# init col with player name column
    column_data=[ ('Player',[]) ]

    i=1
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        # print (f'{i} {name}')
        column_data.append((name,[]))

    for j in range(1,num_week):
        #T is our j'th row
        row_elements=tr_elements[j]

        column_data[0][1].append(player_name)

        #i is the index of our column
        i=1
        #Iterate through each element of the row
        for cell_data in row_elements.iterchildren():
            data=cell_data.text_content()
            #Check if row is empty
            #Convert any numerical value to integers
            try:
                data = data.replace('*','')
                if data == '-':
                    data = 0
                data=int(data)
            except:
                pass
            #Append the data to the empty list of the i'th column
            column_data[i][1].append(data)
            #Increment i for the next column
            i+=1

    # print([len(C) for (title,C) in column_data])

    my_dict={title:column for (title,column) in column_data}
    df=pd.DataFrame(my_dict)
    return df
    # print(df.head())
    # export=df.to_csv(r'mike_evans.csv', index=None, header=True)
