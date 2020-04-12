# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from datetime import date
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt    
import smtplib 
from email.message import EmailMessage
import imghdr
import matplotlib.image as mpimg
from datetime import date, datetime, timedelta
plt.style.use('fivethirtyeight')
url = "https://www.worldometers.info/coronavirus/"
r = requests.get(url)

data = r.text

soup = BeautifulSoup(data, 'html.parser')

live_data = soup.find_all('div', id = 'maincounter-wrap')
for i in live_data:
    print(i.text)
    
    

table_body = soup.find('tbody')
table_rows = table_body.find_all('tr')


countries = []
cases = []
todays = []
deaths = []


for tr in table_rows:
    td = tr.find_all('td')
    countries.append(td[0].text)
    cases.append(td[1].text)
    todays.append(td[2].text)
    deaths.append(td[3].text)
    
cases = [i.replace(',', '') for i in cases]
cases = [int(i) for i in cases]


todays = [i.replace('+', '') for i in todays]
todays = [i.replace(' ', '') for i in todays]
todays = [i.replace(',', '') for i in todays]


for i in range(len(todays)):
    if len(todays[i]) == 0:
        todays[i] = todays[i].replace('', '0')
        
        
        
        
        
for i in range(len(todays)):
    if len(todays[i]) == 0:
        todays[i] = todays[i].replace('', '0')
    else:
        todays[i] = todays[i]
        
        
todays = [int(i) for i in todays]        
        
        
deaths = [i.replace(',', '') for i in deaths]
deaths = [i.replace(' ', '') for i in deaths]       
        
        
for i in range(len(deaths)):
    if len(deaths[i]) == 0:
        deaths[i] = deaths[i].replace('', '0')
    else:
        deaths[i] = deaths[i]
        
        
deaths = [int(i) for i in deaths]        
        
headers = ['countries', 'Total cases', 'Today cases', 'deaths']
df = pd.DataFrame(list(zip(countries, cases, todays, deaths)), columns=headers)        
df['countries'] = df.countries.str.replace(' ', '')

b = df.sort_values('Today cases', ascending = False).head(15)
b = b.to_html(index = False)        
        
a = df[df['countries'] == 'Canada'].reset_index(drop = True)       
Canada= a.to_html(index = False)
c = Canada + b


CA_data = pd.read_csv('/Users/mengn/Covid_CA.csv')

data_today = pd.DataFrame({'Date':[date.today()],
                           'New_Cases' :[a['Today cases'].loc[0]]}).reset_index(drop = True)


data_combine = CA_data.append(data_today).reset_index(drop = True)
data_combine.to_csv('/Users/mengn/Covid_CA.csv', index = False)
plot = data_combine.plot(x = 'Date', y ='New_Cases', color = '#e5ae38', label = 'Canada')
fig = plot.get_figure()
fig.savefig("/Users/mengn/Covid_19.jpg")                 
                  
                  
msg = EmailMessage()
msg['Subject'] = 'latest Covid-19 Update'
msg['From'] = 'mengnan188@gmail.com'
msg['To'] = ['mengnan188@gmail.com']
#msg.set_content(c)
msg.add_alternative(c, subtype = 'html')
with open ('/Users/mengn/Covid_19.jpg', 'rb') as f:
    file_data = f.read()
    file_type = imghdr.what(f.name)
    file_name = f.name

msg.add_attachment(file_data, maintype = 'image', subtype = file_type, filename = file_name)
        
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    
    smtp.login('mengnan188@gmail.com', 'zmn1995228')

    smtp.send_message(msg)        
        
        
    
    
    
    
    
    


