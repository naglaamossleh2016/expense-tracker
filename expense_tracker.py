import tkinter as tk
from tkinter import OptionMenu, ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import json
import requests

payload = {}
headers = {
    "apikey": "6Hm25XXamrWza0StHe1WaFZNhWpXnzEP"
}
def show_expense_in_dollar():
    total = 0.0
    for child in tree.get_children():
        amount = float(tree.item(child, 'values')[0])
        from_cur = tree.item(child, 'values')[1]
        total += float(convert_currency(amount, from_cur))

    # Delete the existing 'total' row if it exists
    total_item = tree.tag_has('total')
    if total_item:
        tree.delete(total_item)

    tree.insert('', 'end', values=(total, "USD"), tags=('total',))
    tree.tag_configure('total', background='yellow')

def convert_currency(amount, from_cur):
    url = f"https://api.apilayer.com/fixer/convert?to=USD&from={from_cur}&amount={amount}"
    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    if status_code == 200:
        try:
            result = json.loads(response.text)
            return result.get("result")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print(f"Failed to fetch data. Status code: {status_code}")

def insert_data():
    if len(amount_val.get()) == 0:
        messagebox.showwarning("Warning", "Enter Amount") 
    else:
        try:
            amount = float(amount_val.get())
            currency = currency_drop.get()
            category = category_drop.get()
            payment_method = payment_drop.get()
            date = cal.get_date()

            # Delete the existing 'total' row if it exists
            total_item = tree.tag_has('total')
            if total_item:
                tree.delete(total_item)

            # Insert the new expense data
            tree.insert('', 'end', values=(amount, currency, category, payment_method, date))
            #Clear the amount entry value
            amount_val.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Warning", "Amount must be a number")

window = tk.Tk()
window.geometry("1200x600")
window.title("Expense tracker Al-Madrasa")


topFrame = tk.Frame(window)
#amount
amount_lbl=tk.Label(topFrame,text="Amount").grid(row=0)
amount_val=tk.Entry(topFrame,width=30)
amount_val.grid(row=0, column=1,ipady=5,pady=5)
#currency
currency_lbl=tk.Label(topFrame,text="Currency").grid(row=1)
# datatype of menu text 
clicked = tk.StringVar() 
currency_drop = ttk.Combobox( topFrame, textvariable =clicked,width=27 ) 
currency_drop['values']=[ 
    "EUR", 
    "GBP", 
    "USD", 
] 

currency_drop.current(2)
currency_drop.grid(row=1,column=1,pady=5)

#Category
category_lbl=tk.Label(topFrame,text="Category").grid(row=3)

catClicked=tk.StringVar()
category_drop=ttk.Combobox(topFrame,textvariable=catClicked,width=27)
category_drop['values']=[
    "Saving",
    "Gas",
    "Water",
    "Electricity",
    "Food",
    "Medicine",
    "Other"
]
category_drop.current(0)
category_drop.grid(row=3,column=1,pady=5)
#payment method

payment_lbl=tk.Label(topFrame,text="payment Method").grid(row=4)

payClicked=tk.StringVar()
payment_drop=ttk.Combobox(topFrame,textvariabl=payClicked,width=27)
payment_drop['values']=[
    "Paypal",
    "Visa",
    "Cash",
]
payment_drop.current(2)
payment_drop.grid(row=4,column=1,pady=5)

#date
date_lbl=tk.Label(topFrame,text="Date").grid(row=5)
cal=DateEntry(topFrame,selectmode='day',width=27)
cal.grid(row=5,column=1,ipady=5,pady=5)


#button add expense
add_btn=tk.Button(topFrame,text="Add Expense",width=15,command=insert_data,bg="orange")
add_btn.grid(row=6,column=0,pady=5)

#button show expense in dollar
show_btn=tk.Button(topFrame,text="Show Expense In Dollar",command=show_expense_in_dollar,bg="yellow")
show_btn.grid(row=6,column=1,pady=5)

topFrame.pack()

#bottom frame for data
bottomFram=tk.Frame(window,width=500)
# define columns
columns = ('Amount', 'Currency', 'Category','Payment_Method','Date')

tree = ttk.Treeview(bottomFram, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col, anchor='center')
    tree.column(col, anchor='center')


# add a scrollbar

tree.grid(row=0,column=1)
scrollbar = ttk.Scrollbar(bottomFram, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=2, sticky='ns')
bottomFram.pack()


window.mainloop()