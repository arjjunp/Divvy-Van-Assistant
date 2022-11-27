import pandas as pd
from .create_station import Station
from .create_task import Tasks
import pymongo


class Operations:
    def __init__(self, radius: int, logins: int) -> None:
        self.select_radius = radius
        self.login_counter = logins
        self.set_terminal_parameters()
        self.host = 'localhost'
        self.port = '27017'
        self.dataset = self.import_dataset()

    def set_terminal_parameters(self) -> None:
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

    def import_dataset(self) -> pd.DataFrame:
        myclient = pymongo.MongoClient("mongodb://" + self.host + ":" + self.port + "/")

        mydb = myclient["Divvy_db"]
        station_table = mydb["Stations"]

        cursor = station_table.find()
        dataset = pd.DataFrame(cursor)

        return dataset

    def run(self) -> list:
        subset_dataset = self.generate_subset_dataset()

        excess_list, deficit_list = self.generate_stations_list(subset=subset_dataset)

        tasks_list = self.generate_tasks_list(esl=excess_list, dsl=deficit_list)

        return tasks_list

    def generate_subset_dataset(self) -> pd.DataFrame:
        col = ' Distance from Base (TBH)'
        return self.dataset.loc[self.dataset[col] <= self.select_radius]

    def generate_stations_list(self, subset: pd.DataFrame) -> list:
        esl = []
        dsl = []
        for index, row in subset.iterrows():
            station = Station(row, index)
            if station.status == 'Excess':
                esl.append(station)
            elif station.status == 'Deficit':
                dsl.append(station)
        dsl.sort(key=lambda c: abs((c.bikes_available) - (c.docks / 2)), reverse=True)
        esl.sort(key=lambda c: abs((c.bikes_available) - (c.docks / 2)), reverse=True)
        return esl, dsl

    def generate_tasks_list(self, esl: list, dsl: list) -> list:
        gtl = []
        start_base = False
        station_visited = []

        if self.login_counter == 1:
            start_base = True

        for d_station in dsl:
            task = Tasks()
            task.initialize_required_params(d_station)
            task.update_end_station()
            task.update_bikes_required()

            if start_base is not True:
                station_visited = task.update_start_station(esl, station_visited)

            task.update_optimal_route()
            task.display_details()

            if len(task.optimal_path) > 0 and task.bikes_required > 5:
                gtl.append(task)

        return gtl
