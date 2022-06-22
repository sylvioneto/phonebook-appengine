import csv
import requests
import json


with open('/Users/sylvio/Downloads/MOCK_DATA.csv', newline='') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in spamreader:
        contact = {"first_name": row[0], "last_name":row[1], "email":row[2], "phone_number":row[3], "country_code":row[4]}
        headers = {'Content-type': 'application/json'}

        print(contact)
        host = 'https://phonebook.sylvio.demo.altostrat.com/api/save'
        x = requests.post(host, headers=headers, data=json.dumps(contact))
        print(x.text)
