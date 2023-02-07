import customtkinter
import tkinter
import main

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# This will also be nice
class TabFrame(customtkinter.CTkFrame):
    def __init__(self, *args, name, default="", **kwargs):
        super().__init__(*args, **kwargs)
        self.width=500
        self.height=500

class EntryBox(customtkinter.CTkFrame):
    def __init__(self, *args, name, default="", **kwargs):
        super().__init__(*args, **kwargs)
        self.width=500
        self.height=500
        self.name = name
        self.default = default
        self.header = customtkinter.CTkLabel(self, text=self.name)
        self.header.pack(padx=3, pady=3)
        self.entry = customtkinter.CTkEntry(self, placeholder_text=self.name)
        self.entry.insert("0", self.default)
        self.entry.pack(padx=3, pady=3)
    
    def get(self):
        return self.entry.get()

class DateSubscription(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Date"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack(padx=20, pady=10)
        def update_names(nothing):
            self.name.configure(values=["--Update--"] + account.shownames())
        self.name = customtkinter.CTkComboBox(master=self,
                                     values=["--Update--"] + account.shownames(), command=update_names)
        self.name.pack(padx=20, pady=10)
        self.date =  EntryBox(self, name="Date", default="2023-02-1") #datetime Or 2 part drop down menu
        self.date.pack()
       
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=20, pady=10)
        
    def add(self):
        account.add_date(self.name.get(), self.date.get())


class SubscriptionPayment(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Subscription Payment"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack(padx=20, pady=10)
        self.name = EntryBox(self, name="name")
        self.name.pack()
        self.amount = EntryBox(self, name="Amount", default="1")
        self.amount.pack()
        self.day =  EntryBox(self, name="Day", default="1")
        self.day.pack()
        self.frequency = customtkinter.CTkOptionMenu(self,
                                       values=["Day", "Week", "Month", "Year"])
        self.frequency.set("Month")
        self.frequency.pack(padx=20, pady=10)
        self.length =  EntryBox(self, name="Lenth", default="1")
        self.length.pack()
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=20, pady=10)
        
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


class ConditionalSubscription(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Condition"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack()
        def update_names(nothing):            
            self.name.configure(values=["--Update--"] + account.shownames())
        self.name = customtkinter.CTkComboBox(master=self,    
                                     values=["--Update--"] + account.shownames(), command=update_names)
        self.name.pack(padx=20, pady=10)
        self.amount =  EntryBox(self, name="Amount")
        self.amount.pack()
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=20, pady=10)
        
    def add(self):
        account.add_investment(int(self.amount.get()), self.name.get())


class ShowPayments(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Show"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        
        textbox = customtkinter.CTkTextbox(master=self, width=500, height=500)
        textbox.pack()

        def show():
            account.drop_account()
            account.sort_budgets()
            textbox.delete("0.0", "100000.100000")
            for item in account.show():
                textbox.insert("0.0", str(item) + "\n")
            textbox.pack()

        self.button = customtkinter.CTkButton(master=self, text="SHOW", command=show)
        self.button.pack(padx=20, pady=10)

class PaymentType(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabview = customtkinter.CTkTabview(self, width=700, height=700)
        self.tabview.pack(padx=30, pady=30)

        self.tabview.add("Subscription")
        self.tabview.add("Condition")
        self.tabview.add("Date")
        self.tabview.add("Show")
        self.tabview.set("Subscription") 
        
        self.tab_subscription = SubscriptionPayment(self.tabview.tab("Subscription"), width=500, height=500)
        self.tab_subscription.pack(padx=20, pady=20)
        self.tab_condition = ConditionalSubscription(self.tabview.tab("Condition"), width=500, height=500)
        self.tab_condition.pack(padx=20, pady=20)
        self.tab_date = DateSubscription(self.tabview.tab("Date"), width=500, height=500)
        self.tab_date.pack(padx=20, pady=20)
        self.tab_show = ShowPayments(self.tabview.tab("Show"), width=500, height=500)
        self.tab_show.pack(padx=20, pady=20)

        self.button = customtkinter.CTkButton(self, text="Reset", command=account.dropall)
        self.button.pack(padx=20, pady=10)


account = main.Bank("myaccount", 0)
app = PaymentType()
app.mainloop()

