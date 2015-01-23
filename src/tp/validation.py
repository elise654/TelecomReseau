'''
Created on 2015-01-21

@author: Elise
'''

import requests
import csv

def check_ssl(url):
    try:
        req = requests.get(url, verify=True)
        print url + ' a un certificat SSL valide!'
    except requests.exceptions.SSLError:
        print url + ' a un certificat SSL invalide!'
        
        
if __name__ == "__main__":
    with open('../../googletop1000april2010.csv','rb') as file:
        contents = csv.reader(file)
        list = []
        for row in contents:
            list.append(row)

        for row in list:
            print row
    check_ssl('http://www.facebook.com')