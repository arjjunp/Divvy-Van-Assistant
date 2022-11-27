import pymongo
import pandas as pd
import json
import os

curr_path = os.getcwd()
dataset_path = curr_path + '\databases\Stations_dataset.csv'


def get_collection() -> None:
    """
    Starts the Mongodb server and returns the Bikes collection which is the Divvy Dataset
        Parameters:
            None

        Returns:
            mytable: pymongo.collection.Collection
                The table that contains the divvy dataset
    """
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Divvy_db"]
    mytable = mydb["Stations"]

    if mytable.estimated_document_count() == 0:
        dataset = pd.read_csv(dataset_path)
        payload = json.loads(dataset.to_json(orient='records'))
        mytable.insert_many(payload)

    return mytable
