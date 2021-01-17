#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 22:41:45 2020

@author: matt
"""

import pandas as pd
import csv
import time
import datetime
from requests import get
from notifypy import Notify
from bs4 import BeautifulSoup
from sys import argv


class CryptoNotifier(object):
    
    def __init__(self, btc_url='https://www.coindesk.com/price/bitcoin', eth_url='https://www.coindesk.com/price/ethereum'):
        self.btc_url = btc_url
        self.eth_url = eth_url
        self.btc_price = '0'
        self.eth_price = '0'
        self.btc_update = '0'
        self.eth_update = '0'
        
        # Initial values are strings, because Notify extension does not accept integers.
        
        
    def find_btc_price(self): # Method obtains the bitcoin price.
        bitcoin_page = get(self.btc_url)
        bs = BeautifulSoup(bitcoin_page.content, features="lxml")
        location = bs.find('div', class_='price-large')
        self.btc_price = location.get_text()
        
        return self.btc_price
    
        
    def find_ethernum_price(self): # Method obtains the etherneum price.
        ethernum_page = get(self.eth_url)
        bs = BeautifulSoup(ethernum_page.content, features='lxml')
        location = bs.find('div', class_='price-large')
        self.eth_price = location.get_text()
        
        return self.eth_price
        
    
    def compute_data(self): # Inserts date and prices into CSV file and calculating how much the values have changed from the last update.
        self.find_btc_price()
        self.find_ethernum_price()
        features = [datetime.datetime.today(), self.btc_price, self.eth_price]
        with open('data.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(features)
        
        frame = pd.read_csv('data.csv', error_bad_lines=False) # Accessing the CSV file for calculations.
        invalid_char = ["$", ","] # Characters which will be removed due to computation reasons.
        data_values = []
        
        for i in range(1,3): # Creating a list of prices.
            for j in range(1,3):
                data_value = frame.iloc[-i,j]
                update_value = data_value.replace(invalid_char[0], '')
                update_value = update_value.replace(invalid_char[1], '')
                data_values.append(update_value)
                
        
        # Calculating the updated value proportion to the previous one (in percentages).       
        delta_btc = (float(data_values[0]) - float(data_values[2]))/float(data_values[2]) * 100
        delta_eth = (float(data_values[1]) - float(data_values[3]))/float(data_values[3]) * 100
        
        self.btc_update = str(delta_btc) + '%'
        self.eth_update = str(delta_eth) + '%'
        
    
    def get_notification(self): # Method which sends a notification to a user.
        self.compute_data()
        crypto_price = (self.btc_price, self.btc_update, self.eth_price, self.eth_update)
        
        while True:
        # Checking if the user wants to get an update for both cryptocurrencies.
            if 'btc' in argv:
                crypto.find_btc_price()
            if 'eth' in argv:
                crypto.find_ethernum_price()
                
            notification = Notify()
            notification.icon = 'btc.png'
            notification.title = "Cryptocurrency Price Notification"
            notification.message = "BTC price: {0} ({1})\nETH price: {2} ({3})".format(*crypto_price)
            notification.send()
            time.sleep(60*10) # Scripts runs every 10 minutes.


if __name__ == "__main__":
    crypto = CryptoNotifier()
    crypto.get_notification()
