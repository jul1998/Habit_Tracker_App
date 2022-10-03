import json
import tkinter.messagebox
import webbrowser
from tkinter import *
import tkinter as tk
from tkcalendar import *
import requests
from conf import Configure


with open("sample.json", "r") as json_file:
    account_data = json.load(json_file)
    USERNAME = account_data["username"]
    TOKEN = account_data["token"]

with open("graph.json", "r") as graph_file:
    graph_data = json.load(graph_file)
    GRAPH_ID = graph_data["GraphTest1"]["id"]


headers = {
    "X-USER-TOKEN": TOKEN
}


def create_Account():
    conf1 = Configure()
    return conf1



graph_url = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}"
graph_url_html = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}.html"



root = tk.Tk()
root.title("Habit Tracker")
root.geometry("400x400")
root.config(padx=70)

#-----------------------------Functions-------------------------------------------
#Format date
def format_date():
    cal.config(date_pattern="yyyyMMdd")
    date = cal.get_date()
    cal.config(date_pattern="dd-mm-y")
    return date


#Add Function
def add_pixel():
    date = format_date()
    try:
        user_input = int(habit_entry.get())
    except ValueError:
        tkinter.messagebox.showerror(title="Not a number", message="Please, enter an interger")
    else:
        print(date)
        add_pixel_parameters = {
            "date": date,
            "quantity": str(user_input),
        }
        response = requests.post(url=graph_url, json=add_pixel_parameters, headers=headers)
        print(response)
        tkinter.messagebox.showinfo(title="Success!", message=f"You have added {user_input} hours in {cal.get_date()}")

def update_pixel():
    date = format_date()
    graph_url_with_date = f"https://pixe.la/v1/users/julian152498/graphs/graph1/{date}"
    try:
        user_input = int(habit_entry.get())
    except ValueError:
        tkinter.messagebox.showerror(title="Not a number", message="Please, enter an interger")
    else:
        print(date)
        update_pixel_parameters = {
            "date": date,
            "quantity": str(user_input),
        }

        response = requests.put(url=graph_url_with_date, json=update_pixel_parameters, headers=headers)
        print(response)
        tkinter.messagebox.showinfo(title="Success!", message=f"You have updated {user_input} hours in {cal.get_date()}")


def delete_pixel():
    date = format_date()
    graph_url_with_date = f"https://pixe.la/v1/users/julian152498/graphs/graph1/{date}"
    ask_question = tkinter.messagebox.askyesno(
        title="Are you sure?",
        message=f"Are you sure that you want to remove pixel from day {cal.get_date()}")
    if ask_question:
        response = requests.delete(url=graph_url_with_date, headers=headers)
        print(response)
        tkinter.messagebox.showinfo(title="Success!",
                                        message=f"You have deleted pixel from day {cal.get_date()}")
    else:
        tkinter.messagebox.showinfo(title="Nothing was deleted", message="Anything has been deleted.")

def show_journey():
    webbrowser.open_new(graph_url_html)


#-----------------------------UI-------------------------------------------

cal = Calendar(root, selectmode="day", year=2022, month=9, day=29, background="black")
cal.grid(column=0, row=0,columnspan=2, pady=30)
#format_date()
#Label
habit_label = Label(text="Enter number of hours, days...")
habit_label.grid(column=0,row=1, sticky=W)

#entry for enter hours, days, Km
habit_entry = Entry()
habit_entry.grid(column=1,row=1, sticky=W)

#Buttons
add_button = Button(text="Add", height=2, width=10, command=add_pixel)
add_button.grid(column=0, row=2, pady=5)

update_button = Button(text="Update", height=2, width=10, command=update_pixel)
update_button.grid(column=1,row=2)

delete_button = Button(text="Delete", height=2, width=10, command=delete_pixel)
delete_button.grid(column=0,row=3)

show_journey_button = Button(text="Show Journey", height=2, width=10, command=show_journey)
show_journey_button.grid(column=1, row=3)


create_account_button = Button(text="Create new account", command= create_Account)
create_account_button.grid(column=0, row=4, pady=5)


root.mainloop()