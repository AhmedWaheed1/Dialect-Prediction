# DataSet Fetching & cleaning
import re
#Text cleaning by regex to replace all bits except arabic letters by spaces
#remove [ English letters , numbers , special characters , ... ] as They not affect on The dialect
match = r'[^\u0020\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD]+'

import requests
import csv
with open('dialect_dataset_cleaned.csv', 'w',encoding='UTF16', newline='') as f:
    csv.writer(f).writerow(["id","dialect","text"]) # write header

import pandas
dataset = pandas.read_csv('dialect_dataset.csv')
id = dataset['id']

for i in range(0 , 459000 , 1000) : # step = 1000 to be sent
    request_body = [''] * 1000
    index = 0
    for j in range( i , i+1000 ) :
        request_body[index] = str(id[j])
        index = index +1

    response = requests.post("https://recruitment.aimtechnologies.co/ai-tasks",
                             json = request_body).json()

    for j in range(i,i+1000):
        text = re.sub( match , ' ' , response[ str(id[j]) ] ) # regex
        text = ' '.join(text.split()) # replace spaces by only 1 space
        
        with open('dialect_dataset_cleaned.csv', 'a', encoding='UTF16', newline='') as f:
            csv.writer(f).writerow([ # write data
                    id[j],
                    dataset['dialect'] [j],
                    text
                    ])