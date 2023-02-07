import customtkinter
import tkinter
import main

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

width_box_level_0 = 1000 
height_box_level_0 = 500 
width_box_level_1 = 800 
height_box_level_1 = 400 
width_box_level_2 = 600 
height_box_level_2 = 300 
width_box_level_3 = 400 
height_box_level_3 = 200 
width_box_level_4 = 200 
height_box_level_4 = 100 
padx_level_1=30
pady_level_1=25
padx_level_2=25
pady_level_2=20
padx_level_3=20
pady_level_3=15
padx_level_4=15
pady_level_4=10
width_entry=500
height_entry=30

# This will also be nice
class TabFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width=width_box_level_1
        self.height=height_box_level_1

class EntryBox(customtkinter.CTkFrame):
    def __init__(self, *args, name, default="", **kwargs):
        super().__init__(*args, **kwargs)
        self.width=width_box_level_2
        self.height=height_box_level_2
        self.name = name
        self.default = default
        self.header = customtkinter.CTkLabel(self, text=self.name)
        self.header.pack(padx=padx_level_4, pady=pady_level_4)
        self.entry = customtkinter.CTkEntry(self, placeholder_text=self.name)
        self.entry.insert("0", self.default)
        self.entry.pack(padx=padx_level_4, pady=pady_level_4)
    
    def get(self):
        return self.entry.get()

class DateSubscription(TabFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Date"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack(padx=padx_level_3, pady=pady_level_3)
        def update_names(nothing):
            self.name.configure(values=["--Update--"] + account.show_dates_not_investments())
        self.name = customtkinter.CTkComboBox(master=self,
                                     values=["--Update--"] + account.show_dates_not_investments(), command=update_names)
        self.name.pack(padx=padx_level_4, pady=pady_level_4)
        self.date =  EntryBox(self, name="Date", default="2023-02-1") #datetime Or 2 part drop down menu
        self.date.pack(padx=padx_level_4, pady=pady_level_4)
       
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=padx_level_4, pady=pady_level_4)
        
    def add(self):
        account.add_date(self.name.get(), self.date.get())


class SubscriptionPayment(TabFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Subscription Payment"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack(padx=padx_level_3, pady=pady_level_3)
        self.name = EntryBox(self, name="name")
        self.name.pack(padx=padx_level_4, pady=pady_level_4)
        self.amount = EntryBox(self, name="Amount", default="1")
        self.amount.pack(padx=padx_level_4, pady=pady_level_4)
        self.day =  EntryBox(self, name="Day", default="1")
        self.day.pack(padx=padx_level_4, pady=pady_level_4)
        self.frequency = customtkinter.CTkOptionMenu(self,
                                       values=["Day", "Week", "Month", "Year"])
        self.frequency.set("Month")
        self.frequency.pack(padx=padx_level_4, pady=pady_level_4)
        self.length =  EntryBox(self, name="Length", default="1")
        self.length.pack(padx=padx_level_4, pady=pady_level_4)
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=padx_level_4, pady=pady_level_4)
        
    def period(self, period):
        if period == "Day":
            return "D"
        if period == "Week":
            return "W"
        if period == "Month":
            return "M"
        if period == "Year":
            return "Y"
        
    def add(self):
        print(self.name.get())
        account.add_payment(self.name.get(), int(self.amount.get()), int(self.day.get()), int(self.length.get()), self.period(self.frequency.get()))


class ConditionalSubscription(TabFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Condition"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack(padx=padx_level_3, pady=pady_level_3)
        def update_names(nothing):            
            self.name.configure(values=["--Update--"] + account.show_investments_not_dates())
        self.name = customtkinter.CTkComboBox(master=self,    
                                     values=["--Update--"] + account.show_investments_not_dates(), command=update_names)
        self.name.pack(padx=padx_level_4, pady=pady_level_4)
        self.amount =  EntryBox(self, name="Amount")
        self.amount.pack(padx=padx_level_4, pady=pady_level_4)
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=padx_level_4, pady=pady_level_4)
        
    def add(self):
        account.add_investment(int(self.amount.get()), self.name.get())


class ShowPayments(TabFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Show"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        
        textbox = customtkinter.CTkTextbox(master=self, width=500, height=500)
        textbox.pack(padx=padx_level_3, pady=pady_level_3)

        def show():
            account.drop_account()
            account.sort_budgets()
            textbox.delete("0.0", "100000.100000")
            for item in account.showall():
                textbox.insert("0.0", str(item) + "\n")
            textbox.pack()

        self.button = customtkinter.CTkButton(master=self, text="SHOW", command=show)
        self.button.pack(padx=padx_level_4, pady=pady_level_4)

class PaymentType(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width_box_level_0
        self.height = width_box_level_0
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.pack(padx=padx_level_1, pady=pady_level_1)

        self.tabview.add("Subscription")
        self.tabview.add("Condition")
        self.tabview.add("Date")
        self.tabview.add("Show")
        self.tabview.set("Subscription") 
        
        self.tab_subscription = SubscriptionPayment(self.tabview.tab("Subscription"))
        self.tab_subscription.pack(padx=padx_level_2, pady=pady_level_2)
        self.tab_condition = ConditionalSubscription(self.tabview.tab("Condition"))
        self.tab_condition.pack(padx=padx_level_2, pady=pady_level_2)
        self.tab_date = DateSubscription(self.tabview.tab("Date"))
        self.tab_date.pack(padx=padx_level_2, pady=pady_level_2)
        self.tab_show = ShowPayments(self.tabview.tab("Show"))
        self.tab_show.pack(padx=padx_level_2, pady=pady_level_2)

        self.button = customtkinter.CTkButton(self, text="Reset", command=account.dropall)
        self.button.pack(padx=padx_level_1, pady=pady_level_1)


account = main.Bank("myaccount", 0)
app = PaymentType()
app.mainloop()
