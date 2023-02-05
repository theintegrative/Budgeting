#!/usr/bin/env python
# coding: utf-8

import customtkinter
import tkinter


import main


customtkinter.set_appearance_mode("dark")


customtkinter.set_default_color_theme("dark-blue")


class DateSubscription(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Date"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack(padx=20, pady=10)
        self.name = customtkinter.CTkEntry(self,  placeholder_text="Name")
        self.name.pack(padx=20, pady=10)
        self.amount = customtkinter.CTkEntry(self, placeholder_text="yyyy-mm-dd")
        self.amount.pack(padx=20, pady=10)
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=20, pady=10)
        
    def add(self):
        print("ADD")


class SubscriptionPayment(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Subscription Payment"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack(padx=20, pady=10)
        self.name = customtkinter.CTkEntry(self,  placeholder_text="Name")
        self.name.pack(padx=20, pady=10)
        self.amount = customtkinter.CTkEntry(self, placeholder_text="Amount")
        self.amount.pack(padx=20, pady=10)
        self.day =  customtkinter.CTkEntry(self, placeholder_text="Day")
        self.day.pack(padx=20, pady=10)
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=20, pady=10)
        
    def add(self):
        print("ADD")


class ConditionalSubscription(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Condition"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack(padx=20, pady=10)
        self.name = customtkinter.CTkEntry(self,  placeholder_text="Name")
        self.name.pack(padx=20, pady=10)
        self.amount = customtkinter.CTkEntry(self, placeholder_text="Amount")
        self.amount.pack(padx=20, pady=10)
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=20, pady=10)
        
    def add(self):
        print("ADD")


class ShowPayments(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Show"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        
        self.button = customtkinter.CTkButton(master=self, text="SHOW", command=self.show)
        self.button.pack(padx=20, pady=10)
    
    def show(self):
        lst = ['a', 'b', 'c', 'd']
        textbox = customtkinter.CTkTextbox(self)
        for item in lst:
            textbox.insert(f"0.0", item + "\n")
        textbox.pack()
        textbox.configure(state="disabled")


class PaymentType(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20)

        self.tabview.add("Subscription")
        self.tabview.add("Condition")
        self.tabview.add("Date")
        self.tabview.add("Show")
        self.tabview.set("Subscription") 
        
        self.tab_subscription = SubscriptionPayment(self.tabview.tab("Subscription"))
        self.tab_subscription.pack(padx=20, pady=20)
        self.tab_condition = ConditionalSubscription(self.tabview.tab("Condition"))
        self.tab_condition.pack(padx=20, pady=20)
        self.tab_date = DateSubscription(self.tabview.tab("Date"))
        self.tab_date.pack(padx=20, pady=20)
        self.tab_show = ShowPayments(self.tabview.tab("Show"))
        self.tab_show.pack(padx=20, pady=20)


class App(customtkinter.CTk):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.this = PaymentType(master=self)
        self.this.pack()
        self.account = main.Bank("myaccount", 0)
        self.button = customtkinter.CTkButton(master=self, text="Reset", command=self.account.dropall)
        self.button.pack(padx=20, pady=10)


app = App()
app.mainloop()

