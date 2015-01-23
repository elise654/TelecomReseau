'''
Created on 2015-01-21

@author: Elise
'''

import requests

def check_ssl(url):
    try:
        req = requests.get(url, verify=True)
        print url + ' a un certificat SSL valide!'
    except requests.exceptions.SSLError:
        print url + ' a un certificat SSL invalide!'
        
        
if __name__ == "__main__":
    check_ssl('http://www.facebook.com')