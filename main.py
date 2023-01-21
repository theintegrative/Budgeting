from datetime import datetime
import pymongo
import pandas as pd


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
    
    def reset_balance(self):
        self.account.update_many({"balance": {"$gt": -1000000}}, {"$set": {"balance": 0}})
        
    def calculate_balance(self):
        placeholder = 0
        calculated = []
        self.reset_balance()
        for transaction in self.account.find({}, {}).sort([("date", 1)]):
            self.account.delete_one(transaction)
            placeholder += (transaction["debit"] + transaction["credit"])
            transaction["balance"] += placeholder
            self.account.insert_one(transaction)
            
    def fixed_budgets(self, finances):
        for payments in finances:
            payments.dates_now()
            self.transact_many([payment for payment in payments.generate()])
            self.calculate_balance()
    
    def planed_investments(self, investments):
        for investment in investments:
            for transaction in self.show():
                if transaction["balance"] > investment["start"]:
                    payments = investment["payments"]
                    payments.dates_from(transaction["date"])
                    self.transact_many([payment for payment in payments.generate()])
                    self.calculate_balance()
                    break
                
    def show(self):
        return [transaction for transaction in self.account.find({}, {"_id": 0, "name": 1, "date":1, "balance": 1})]
          
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
        self.dates = ""

    def transaction_json(self, date, credit, debit, balance):
        return {"date": date, "name": self.name, "credit": credit, "debit": -debit, "balance": balance}

    def first_day(self):
        now = pd.Timestamp.now()
        now = now - pd.offsets.MonthBegin(self.day)
        return now.strftime('%Y-%m-%d')

    def dates_now(self):    
        def generate():    
            for date in pd.date_range(self.first_day(), periods=self.periods, freq=self.freq):
                moment = pd.Timestamp(date)
                yield moment.strftime('%Y-%m-%d')
        self.dates = generate() 

    def dates_from(self, date):
        def generate(date):
            first_day = datetime.strptime(date, '%Y-%m-%d')
            for date in pd.date_range(first_day, periods=self.periods, freq=self.freq):
                moment = pd.Timestamp(date)
                yield moment.strftime('%Y-%m-%d')
        self.dates = generate(date)

    def generate(self):
        if self.amount < 0:
            return self.generate_debit()
        else:
            return self.generate_credit()

    def generate_credit(self):
        return [self.transaction_json(next(self.dates), self.amount, 0, 0) for _ in range(self.periods)]

    def generate_debit(self):
        return [self.transaction_json(next(self.dates), 0, -self.amount, 0) for _ in range(self.periods)]
