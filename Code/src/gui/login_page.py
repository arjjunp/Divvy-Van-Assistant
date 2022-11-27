import PySimpleGUI as sg
from pymongo import MongoClient
from datetime import datetime
import re
sg.theme('TealMono')


class Login:
    def __init__(self):
        self.db_name = None
        self.collection_name = None
        self.result = None
        self._login_preq()

    # Checking if DIVVY user DB Exists
    def _check_for_db(self):
        client = MongoClient('mongodb://localhost:27017/')
        dblist = client.list_database_names()
        db_instance = client[self.db_name]

        if self.db_name in dblist:
            print("DB Exists")
            collist = db_instance.list_collection_names()
            if self.collection_name in collist:
                print("The collection exists.")
            else:
                mycol = db_instance["users"]
                admin_user = {"email": "admin", "password": "admin", "username": "admin"}
                mycol.insert_one(admin_user)

        else:
            mycol = db_instance["users"]
            admin_user = {"email": "admin", "password": "admin", "username": "admin"}
            mycol.insert_one(admin_user)
            print("DB Created")

    def _login_preq(self):
        self.db_name = 'Divvy_db'
        self.collection_name = "users"
        self.result = False
        self._check_for_db()

    def _progress_bar(self):
        layout = [[sg.Text('Creating your account...')],
                  [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
                  [sg.Cancel()]]

        window = sg.Window('Working...', layout)
        for i in range(1000):
            event, values = window.read(timeout=1)
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            window['progbar'].update_bar(i + 1)
        window.close()

    # Helps in Signning Up
    def create_account(self):
        self._check_for_db()
        layout = [[sg.Text("Sign Up", size=(15, 1), font=40, justification='c')],
                  [sg.Text("E-mail", size=(15, 1), font=16), sg.InputText(key='-email-', font=16)],
                  [sg.Text("Re-enter E-mail", size=(15, 1), font=16), sg.InputText(key='-remail-', font=16)],
                  [sg.Text("Create Username", size=(15, 1), font=16), sg.InputText(key='-username-', font=16)],
                  [sg.Text("Create Password", size=(15, 1), font=16),
                   sg.InputText(key='-password-', font=16, password_char='*')],
                  [sg.Button("Submit"), sg.Button("Cancel")]]

        window = sg.Window("Sign Up", layout)

        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            else:
                if event == "Submit":
                    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    if not (re.fullmatch(regex, values['-email-'])):
                        sg.popup_error("Please make sure the email address follows the pattern: example@email.com")
                        continue

                    if values['-email-'] != values['-remail-']:
                        sg.popup_error("Error: Email does not match", font=16)
                        continue

                    if self._check_if_user_exists(values['-username-']):
                        sg.popup_error("Error: User already exists, Try a different one", font=16)
                        continue

                    else:
                        self._progress_bar()
                        self._add_user(values)
                        self.result = True
                        break

        window.close()
        return self.result

    def _add_user(self, values):
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db_name]
        mycol = mydb[self.collection_name]
        todays_date = datetime.today().strftime('%d-%m-%Y')
        user_dict = {"email": values['-email-'],
                     "username": values['-username-'],
                     "password": values['-password-'],
                     "logins_for_the_day": 0,
                     "user_created_on": todays_date,
                     "login_history": ""}
        mycol.insert_one(user_dict)

        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db_name]
        mycol = mydb['Agg']
        user_dict = {"username": values['-username-'],
                     "Tasks_Completed": 0,
                     "Distance_Driven": 0,
                     "Bikes Transferred": 0,
                     }
        mycol.insert_one(user_dict)

    def _check_if_user_exists(self, username):
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db_name]
        mycol = mydb[self.collection_name]
        x = mycol.find_one({"username": username})
        if x:
            return True
        else:
            return False

    # Helps in signing in to the user account
    def sign_in(self, admin=False):
        self._check_for_db()
        layout = [[sg.Text("Log In", size=(15, 1), font=40)],
                  [sg.Text("Username", size=(15, 1), font=16), sg.InputText(key='-username-', font=16)],
                  [sg.Text("Password", size=(15, 1), font=16),
                   sg.InputText(key='-password-', password_char='*', font=16)],
                  [sg.Button('Ok'), sg.Button('Cancel')]]

        window = sg.Window("Log In", layout)

        while True:
            event, values = window.read()
            if event == "Cancel" or event == sg.WIN_CLOSED:
                break
            else:
                if event == "Ok":
                    if not admin:
                        user = self._fetch_user_details(values['-username-'])
                    else:
                        user = self._fetch_user_details('admin')
                    if user is None:
                        sg.popup("Username does not exists")
                        continue

                    elif (user['username'] == values['-username-']) and (user['password'] == values['-password-']):
                        if not admin:
                            todays_date = datetime.today().strftime('%d-%m-%Y')
                            last_login_date = user["login_history"]
                            query = {"username": user['username']}

                            print("here are the values")
                            print(user)

                            if todays_date != last_login_date:
                                count = 1
                                newvalues = {"$set": {"logins_for_the_day": count, "login_history": todays_date}}
                            else:
                                count = user['logins_for_the_day']
                                count += 1
                                newvalues = {"$set": {"logins_for_the_day": count}}

                            self._update_db_values(query, newvalues)
                        self.result = True
                        sg.popup("Welcome!")
                        break

                    else:
                        sg.popup("Incorrect password. Try again")

        window.close()
        return self.result, values['-username-']

    def _fetch_user_details(self, username):
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db_name]
        mycol = mydb[self.collection_name]
        x = mycol.find_one({"username": username})
        return x

    def _update_db_values(self, query, newvalues):
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db_name]
        mycol = mydb[self.collection_name]
        mycol.update_one(query, newvalues)

    def _update_db_values2(self, query, newvalues):
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db_name]
        mycol = mydb['Agg']
        mycol.update_one(query, newvalues)

    def _fetch_user_details2(self, username):
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db_name]
        mycol = mydb['Agg']
        x = mycol.find_one({"username": username})
        return x
