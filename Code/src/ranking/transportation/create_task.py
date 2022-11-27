from .create_station import Station
from .optimal_route_generation import get_directions


class Tasks:
    def __init__(self) -> None:
        self.start_name = 'UIC - Thomas Beckham Hall (Base)'
        self.start_address = '1250 S Halsted St, Chicago, IL'
        self.start_pluscode = '86HJV983%2B74'
        self.end_name = None
        self.end_address = None
        self.end_pluscode = None
        self.bikes_required = None
        self.travel_distance = None
        self.optimal_path = None

    def initialize_required_params(self, deficit: Station) -> None:
        self.deficit_station = deficit

    def update_end_station(self) -> None:
        self.end_name = self.deficit_station.name
        self.end_address = self.deficit_station.address
        self.end_pluscode = self.deficit_station.pluscode

    def update_bikes_required(self) -> None:
        difference = (self.deficit_station.docks / 2) - (self.deficit_station.bikes_available)
        self.bikes_required = round(difference)

    def update_start_station_info(self, start_station: Station = None) -> None:
        self.start_name = start_station.name
        self.start_address = start_station.address
        self.start_pluscode = start_station.pluscode

    def update_start_station(self, esl: list, visited: list) -> list:
        for excess in esl:
            cond_1 = excess not in visited
            if cond_1:
                bikes_for_transport = round(excess.bikes_available - (0.5 * excess.docks))
                bikes_required = self.bikes_required

                cond_2 = abs(bikes_for_transport) >= bikes_required
                if cond_2:
                    self.update_start_station_info(start_station=excess)
                    visited.append(excess)
                    return visited
        return visited

    def update_optimal_route(self) -> None:
        org = self.start_pluscode
        dest = self.end_pluscode
        if self.start_address is not None:
            self.optimal_path, self.travel_distance = get_directions(origin=org, destination=dest)

    def display_details(self) -> None:
        print('\n\nStart Station Name:', self.start_name)
        print('Start Station Address:', self.start_address)
        print('End Station Name:', self.end_name)
        print('End Station Address:', self.end_address)
        print('Bikes to be Transportes:', self.bikes_required)
        print('Distance to Travel:', self.travel_distance)
        print('Optimal Route to Follow:', self.optimal_path)
