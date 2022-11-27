import os
import PySimpleGUI as psg
import pymongo
from pymongo import MongoClient
import pandas as pd
from gui.login_page import Login

l = Login()
curr_dir = os.getcwd()

BPAD_TOP = ((20, 20), (20, 10))


class Reports:
    def __init__(self):
        self.db_name = 'Divvy_db'
        self.collection_name = "users"
        self.db_collection = None
        self._update_db_vars()

    def _update_db_vars(self):
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db_name]
        self.db_collection = mydb[self.collection_name]

    def start_page(self):
        layout = [[psg.Text('Divvy Van Assistant', justification='center', pad=BPAD_TOP, font='Any 20')],
                  [psg.Button('Generate Report'), psg.Button('Back')]]
        window = psg.Window('Reports Page', layout, size=(450, 150), finalize=True)

        while True:
            window, event, values = psg.read_all_windows()
            if event in (psg.WIN_CLOSED, 'Back'):
                break

            elif event == 'Generate Report':
                self.generate_report()
                continue

        window.close()

    def generate_report(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Divvy_db"]

        col_users = db["users"]
        users_df = pd.DataFrame(list(col_users.find()))
        users_df.to_csv(curr_dir + '/reports/Users_Report.csv')

        col_logs = db["logs"]
        logs_df = pd.DataFrame(list(col_logs.find()))
        logs_df.to_csv(curr_dir + '/reports/Logs_Report.csv')

        col_agg = db["Agg"]
        agg_df = pd.DataFrame(list(col_agg.find()))
        agg_df.to_csv(curr_dir + '/reports/Driver_Summary_Report.csv')

    def _dailylog(self, username, taskno, seltask):
        self.db_name = 'Divvy_db'
        self.collection_name = "logs"
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient[self.db_name]
        mycol = mydb[self.collection_name]
        user_dict = {"UserName": username,
                     "Task Number": taskno,
                     "Start Station Name": seltask.start_name,
                     "End Station Name": seltask.end_name,
                     "Bikes Transported": seltask.bikes_required,
                     "Distance": seltask.travel_distance
                     }
        mycol.insert_one(user_dict)

    def _update_aggregate(self, username, taskno, seltask):
        user = l._fetch_user_details2(username)
        query = {"username": username}

        task_count = user['Tasks_Completed'] + 1
        bikes_count = user['Bikes Transferred'] + seltask.bikes_required
        distance_count = user['Distance_Driven'] + seltask.travel_distance

        task_newvalues = {"$set": {"Tasks_Completed": task_count}}
        bikes_newvalues = {"$set": {"Bikes Transferred": bikes_count}}
        distance_newvalues = {"$set": {"Distance_Driven": round(distance_count, 2)}}

        l._update_db_values2(query, task_newvalues)
        l._update_db_values2(query, bikes_newvalues)
        l._update_db_values2(query, distance_newvalues)
