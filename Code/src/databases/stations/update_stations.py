import random
import pymongo


def update_station_status(mytable) -> None:
    """
    Updates the status of the Station based on number of bikes available

        Parameters:
            None

        Returns:
            None
    """
    for row in mytable.find():
        if (row["Bikes Available"] >= round(0.6 * row["Total Docks"])):
            mytable.update_one(row, {"$set": {"Station Status": "Excess"}})
        elif (row["Bikes Available"] <= round(0.4 * row["Total Docks"])):
            mytable.update_one(row, {"$set": {"Station Status": "Deficit"}})
        else:
            mytable.update_one(row, {"$set": {"Station Status": "Sufficient Quantity"}})


def random_update_availability(mytable) -> None:
    """
    Randomly updates the number of bikes available at the Station to replicate
    customer usage of bikes.

        Parameters:
            None

        Returns:
            None
    """
    for row in mytable.find():
        prob = random.randrange(0, 10, 1)
        bikes_change = random.randint(0, 10)

        if prob > 5:
            rand_val = row["Bikes Available"] + bikes_change
        else:
            rand_val = row["Bikes Available"] - bikes_change

        if rand_val > row["Total Docks"]:
            rand_val = row["Total Docks"]

        if rand_val < 0:
            rand_val = 0

        mytable.update_one(row, {"$set": {"Bikes Available": rand_val}})


def update_data_completion(data, seltask):
    query = {"Station Name": seltask.end_name}
    end_station = data.find_one(query)

    count = end_station['Bikes Available'] + seltask.bikes_required
    data.update_one(end_station, {"$set": {"Bikes Available": count}})

    update_station_status(data)
