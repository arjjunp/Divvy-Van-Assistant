import requests
import re


def get_directions(origin, destination):
    full_route = []
    total_distance = 0.0
    payload = {}
    headers = {}

    url = "https://maps.googleapis.com/maps/api/directions/json?origin=" +\
        origin + "&destination=" +\
        destination + "&key=AIzaSyBsDGSrKrlv5ARgI-JngR-9IyhW0NtP8ew" +\
        "&avoid=highways|tolls" + "&mode=driving"

    response = requests.request("GET", url, headers=headers, data=payload)

    if len(response.json()['routes']) != 0:
        sub_data = response.json()['routes'][0]['legs'][0]['steps']

        for step in sub_data:
            dist = step['distance']['text']
            total_distance += get_converted_dist(dist)
            route = step['html_instructions']
            route = re.sub("<.*?>", " ", step['html_instructions'])
            route_dist = route + " and travel for " + dist
            full_route.append(route_dist)

    return full_route, round(total_distance, 2)


def get_converted_dist(dist):
    dist_arr = dist.split()
    cdist = 0.0

    if dist_arr[1] == 'ft':
        cdist = float(dist_arr[0]) * 0.00019

    elif dist_arr[1] == 'mi':
        cdist = float(dist_arr[0])

    else:
        print(dist)

    return cdist
