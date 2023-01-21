#!/usr/bin/env python
# coding: utf-8

import pymongo
import pandas as pd


balance = {
      "$setWindowFields": {
         "sortBy": { "date": 1 },
         "output": {
            "balance": {
               "$sum": "$balance",
               "window": {
                  "documents": [ "unbounded", "current" ]
               }
            }
         }
      }
   }


class Bank:
    def __init__(self, account, amount):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mybank = self.client["bank"]
        self.account = self.mybank[account]
        self.starter(amount)
    
    def transact_many(self, transactions):
        self.account.insert_many(transactions)
        
    def starter(self, start_credit):
        now = pd.Timestamp.now()
        date = now.strftime('%Y-%m-%d')
        self.account.insert_one({"date": date, "name": "Initial", "credit": start_credit, "debit": 0, "balance": 0})
        
    def calculate_balance(self):
        placeholder = 0
        calculated = []
        for transaction in self.account.find({}, {}).sort([("date", 1)]):
            self.account.delete_one(transaction)
            placeholder += (transaction["debit"] + transaction["credit"])
            transaction["balance"] += placeholder
            self.account.insert_one(transaction)
          
    def show(self):
        return [transaction for transaction in self.account.find({}, {"_id": 0, "date": 1, "balance": 1})]

    def showall(self):
        return [transaction for transaction in self.account.find({}, {"_id":0})]
    
    def dropall(self):
        self.account.drop()

class payment:
    def __init__(self, name, amount, day, periods, freq="M"):
        self.name = name
        self.amount = amount
        self.day = day
        self.periods = periods
        self.freq = freq
    
    def transaction_json(self, date, credit, debit, balance):
        return {"date": date, "name": self.name, "credit": credit, "debit": -debit, "balance": balance}
        
    def first_day(self):
        now = pd.Timestamp.now()
        now = now - pd.offsets.MonthBegin(self.day)
        return now.strftime('%Y-%m-%d')

    def dates(self):
        for date in pd.date_range(self.first_day(), periods=self.periods, freq=self.freq):
            moment = pd.Timestamp(date)
            yield moment.strftime('%Y-%m-%d')
            
    def generate(self):
        if self.amount < 0:
            return self.generate_debit()
        else:
            return self.generate_credit()

    def generate_credit(self):
        date = self.dates()
        return [self.transaction_json(next(date), self.amount, 0, 0) for _ in range(self.periods)]
            
    def generate_debit(self):
        date = self.dates()
        return [self.transaction_json(next(date), 0, -self.amount, 0) for _ in range(self.periods)]
