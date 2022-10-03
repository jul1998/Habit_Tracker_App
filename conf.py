import datetime
import json

import requests
import tkinter.messagebox
from tkinter import *
import tkinter as tk

PIXELA_ENDPOINT_CREATE_ACCOUNT = "https://pixe.la/v1/users"


class Configure(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.config(padx=10)
        self.title("Create  Account")

        # Change key
        with open("sample.json", "r") as json_file:
            loaded_data = json.load(json_file)
            headers = loaded_data["token"]
            username = loaded_data["username"]
            self.headers = {
                "X-USER-TOKEN": headers
            }
            self.username = username
        with open("graph.json", "r") as graph_file:
            loaded_data = json.load(graph_file)
            graph_id = loaded_data["GraphTest1"]["id"]

        self.PIXELA_GRAPH_ENDPOINT = f"https://pixe.la/v1/users/{self.username}/graphs"
        self.graph_url_html = f"https://pixe.la/v1/users/{self.username}/graphs/{graph_id}.html"
        self.graph_url = f"https://pixe.la/v1/users/{self.username}/graphs/{graph_id}"

        # Labels for creating user
        self.account_id_label = Label(self, text="Please, enter any account id")
        self.account_id_label.grid(column=0, row=0, sticky=W)

        self.username_label = Label(self, text="Please, enter an username")
        self.username_label.grid(column=0, row=1, sticky=W)

        self.token = Label(self, text="Please, enter a token")
        self.token.grid(column=0, row=2, sticky=W)

        self.agree_terms = Label(self,
                                 text="Please, enter 'yes' if you agree with the "
                                      "terms",
                                 )
        self.agree_terms.grid(column=0, row=3, sticky=W)

        self.notMinor_label = Label(self, text="Please, enter 'yes' if you are not minor")
        self.notMinor_label.grid(column=0, row=4, sticky=W)

        # Labels for creating graph
        self.graph_id_label = Label(self, text="Please, enter an ID for your graph")
        self.graph_id_label.grid(column=0, row=6, sticky=W)

        self.graph_name_label = Label(self, text="Please, enter a name for your graph")
        self.graph_name_label.grid(column=0, row=7, sticky=W)

        self.graph_unit_label = Label(self, text="Please, enter an unit for your graph")
        self.graph_unit_label.grid(column=0, row=8, sticky=W)

        self.graph_type_label = Label(self, text="Please, enter a type (int or float) for your graph")
        self.graph_type_label.grid(column=0, row=9, sticky=W)

        self.graph_color_label = Label(self, text="Please, "
                                                  "enter a color for your graph")
        self.graph_color_label.grid(column=0, row=10, sticky=W)

        # Entries for creating account
        self.account_id_entry = Entry(self, width=20)
        self.account_id_entry.grid(column=1, row=0)

        self.username_entry = Entry(self, width=20)
        self.username_entry.grid(column=1, row=1, sticky=W)

        self.token_entry = Entry(self, width=20)
        self.token_entry.grid(column=1, row=2)

        self.agree_terms_entry = Entry(self, width=20)
        self.agree_terms_entry.grid(column=1, row=3)

        self.notMinor_entry = Entry(self, width=20)
        self.notMinor_entry.grid(column=1, row=4)

        # Entries for creating graph
        self.graph_id_entry = Entry(self, width=20)
        self.graph_id_entry.grid(column=1, row=6)

        self.graph_name_entry = Entry(self, width=20)
        self.graph_name_entry.grid(column=1, row=7)

        self.graph_unit_entry = Entry(self, width=20)
        self.graph_unit_entry.grid(column=1, row=8)

        self.graph_type_entry = Entry(self, width=20)
        self.graph_type_entry.grid(column=1, row=9, )

        self.graph_color_entry = Entry(self, width=20)
        self.graph_color_entry.grid(column=1, row=10)

        # Button for creating account
        self.create_account_button = Button(self, text="Create account",
                                            state="normal",
                                            width=20,
                                            command=self.create_account_first_step)
        self.create_account_button.grid(column=0, row=5, pady=5)

        # Button for creating graph
        self.create_graph_button = Button(self,
                                          text="Create graph",
                                          width=20,
                                          command=self.create_graph_second_step)
        self.create_graph_button.grid(column=0, row=11, pady=5)

        self.mainloop()

    def check_entries_to_create_account(self):
        if len(self.username_entry.get()) == 0 or \
                len(self.token_entry.get()) < 8 or \
                (len(self.agree_terms_entry.get()) == 0 or self.agree_terms_entry.get() != "yes") or \
                (len(self.notMinor_entry.get()) == 0 or self.notMinor_entry.get() != "yes"):
            return True

    def create_account_first_step(self):
        if self.check_entries_to_create_account():
            tkinter.messagebox.showerror(title="Something is missing",
                                         message="Please,verify the API documentation since something is not"
                                                 " correct in your entries: https://docs.pixe.la/entry/post-user")
        else:
            self.create_account_button.config(state="disabled")
            USERNAME = self.username_entry.get()
            TOKEN = self.token_entry.get()
            AGREETERMS = self.agree_terms_entry.get()
            NOTMINOR = self.notMinor_entry.get()

            create_account_parameters = {
                "token": TOKEN,
                "username": USERNAME,
                "agreeTermsOfService": AGREETERMS,
                "notMinor": NOTMINOR
            }
            response = requests.post(url=PIXELA_ENDPOINT_CREATE_ACCOUNT, json=create_account_parameters)
            print(response.text)

            # Writing to sample.json
            self.save_data_json()

    def save_data_json(self):
        USERNAME = self.username_entry.get()
        TOKEN = self.token_entry.get()
        new_data = {
            "username": USERNAME,
            "token": TOKEN,
        }
        try:
            with open("sample.json", "r") as data_file:
                read_data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            with open("sample.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            read_data.update(new_data)
            with open("sample.json", "w") as data_file:
                json.dump(read_data, data_file, indent=4)

    def check_entries_to_create_graph(self):
        types = ["int", "float"]
        colors = ["shibafu", "momiji", "sora", "ichou", "ajisai", "kuro"]
        if len(self.graph_id_entry.get()) == 0 or \
                len(self.graph_name_entry.get()) == 0 or \
                len(self.graph_unit_entry.get()) == 0 or \
                self.graph_type_entry.get() not in types or \
                self.graph_color_entry.get() not in colors:
            return True

    def create_graph_second_step(self):
        ID = self.graph_id_entry.get()
        NAME= self.graph_name_entry.get()
        UNIT = self.graph_unit_entry.get()
        TYPE = self.graph_type_entry.get()
        COLOR = self.graph_color_entry.get()
        if self.check_entries_to_create_graph():
            tkinter.messagebox.showerror(title="Something is missing",
                                         message="Please,verify the API documentation since something is not"
                                                 " correct in your entries: https://docs.pixe.la/entry/post-graph")
        else:
            self.create_graph_button.config(state="disabled")
            pixela_graph_parameters = {
                "id": ID,
                "name": NAME,
                "unit": UNIT,
                "type": TYPE,
                "color": COLOR
            }
            response = requests.post(url=self.PIXELA_GRAPH_ENDPOINT, json=pixela_graph_parameters, headers=self.headers)
            print(response.text)
            tkinter.messagebox.showinfo(title="API response", message=response.text)

            print("Right")
            self.save_data_json_graph()


    def save_data_json_graph(self):
        ID = self.graph_id_entry.get()
        NAME= self.graph_name_entry.get()
        UNIT = self.graph_unit_entry.get()
        TYPE = self.graph_type_entry.get()
        COLOR = self.graph_color_entry.get()
        new_data = {
            NAME: {
                "id": ID,
                "graph_name": NAME,
                "unit": UNIT,
                "type": TYPE,
                "color":COLOR
            }

        }
        try:
            with open("graph.json", "r") as data_file:
                read_data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            with open("graph.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            read_data.update(new_data)
            with open("graph.json", "w") as data_file:
                json.dump(read_data, data_file, indent=4)