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
        self.btc_upd = '0'
        self.eth_upd = '0'
        
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
        error_char = ["$", ","] # Characters which will be removed due to computation reasons.
        data_values = []
        updates = []
        
        for i in range(1,3): # Creating a list of prices.
            for j in range(1,3):
                data_values.append(frame.iloc[-i,j]) # Getting last two prices (including the most recent one) for comparison.
                
                
        for value in range(len(data_values)): # Removing aforementioned characters.
            upd_val = data_values[value].replace(error_char[0], '')
            upd_val = upd_val.replace(error_char[1], '')
            updates.append(upd_val)
        
        # Calculating the updated value proportion to the previous one (in percentages).       
        delta_btc = (float(updates[0]) - float(updates[2]))/float(updates[2]) * 100
        delta_eth = (float(updates[1]) - float(updates[3]))/float(updates[3]) * 100
        
        self.btc_upd = str(delta_btc) + '%'
        self.eth_upd = str(delta_eth) + '%'
        
    
    def get_notification(self): # Method which sends a notification to a user.
        self.compute_data()
        
        while True:
        # Checking if the user wants to get an update for both cryptocurrencies.
            if 'btc' in argv:
                crypto.find_btc_price()
            if 'eth' in argv:
                crypto.find_ethernum_price()
                
            notification = Notify()
            notification.icon = 'btc.png'
            notification.title = "Cryptocurrency Price Notification"
            notification.message = "BTC price: %s (%s)\nETH price: %s (%s)" % (self.btc_price, self.btc_upd, self.eth_price, self.eth_upd)
            notification.send()
            time.sleep(60*10) # Scripts runs every 10 minutes.


if __name__ == "__main__":
    crypto = CryptoNotifier()
    crypto.get_notification()
