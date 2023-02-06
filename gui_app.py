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
        def update_names(nothing):
            self.name.configure(values=account.shownames())
        self.name = customtkinter.CTkComboBox(master=self,
                                     values=account.shownames(), command=update_names)
        self.name.pack(padx=20, pady=10)
        self.date = customtkinter.CTkEntry(self, placeholder_text="yyyy-mm-dd")
        self.date.pack(padx=20, pady=10)
       
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
        self.name = customtkinter.CTkEntry(self,  placeholder_text="Name")
        self.name.pack(padx=20, pady=10)
        self.amount = customtkinter.CTkEntry(self, placeholder_text="Amount")
        self.amount.pack(padx=20, pady=10)
        self.day =  customtkinter.CTkEntry(self, placeholder_text="Day")
        self.day.pack(padx=20, pady=10)
        self.months =  customtkinter.CTkEntry(self, placeholder_text="Months")
        self.months.pack(padx=20, pady=10)
        self.button = customtkinter.CTkButton(master=self, text="ADD", command=self.add)
        self.button.pack(padx=20, pady=10)
        
        def combobox_callback():
            print("Lol")

        self.combobox = customtkinter.CTkComboBox(self,
                                     values=["option 1", "option 2"],
                                     command=combobox_callback)
        self.combobox.pack(padx=20, pady=10)

        
    def add(self):
        print(self.name.get())
        account.add_payment(self.name.get(), int(self.amount.get()), int(self.day.get()), int(self.months.get()))


class ConditionalSubscription(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = "Condition"
        self.header = customtkinter.CTkLabel(self, text=self.header_name)
        self.header.pack()
        def update_names(nothing):            
            self.name.configure(values=account.shownames())
        self.name = customtkinter.CTkComboBox(master=self,    
                                     values=account.shownames(), command=update_names)
        self.name.pack(padx=20, pady=10)
        self.amount = customtkinter.CTkEntry(self, placeholder_text="Amount")
        self.amount.pack(padx=20, pady=10)
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
        # textbox.configure(state="disabled")

        def show():
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

