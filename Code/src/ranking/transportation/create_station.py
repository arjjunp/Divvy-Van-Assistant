import pandas as pd


class Station:
    """
    A class to represent a Divvy Station.

    Attributes:
        id : int
            Represents the Divvy station ID (default = None)
        name : str
            Represents the Divvy station Name (default = None)
        address : str
            Represents the Divvy station Address (default = None)
        docks : int
            Represents the total number of docks available at Divvy station
            (default = None)
        bikes_available : int
            Represents the total bikes available at Divvy station
            (default = None)
        status : str
            Represents whether the Divvy station is in Excess, Deficit or
            Sufficient Quantity (default = None)
        distance_ref : int
            Represents the distance of the Divvy station from UIC TBH as base
            (default = None)
        zipcode : int
            Represents the zipcode of the Divvy Station
            (default = None)

    Methods:
        generate_series_axes():
            Returns names of attributes in row.
        update_static_variables():
            Updates the static variables of the class based on details
            from dataset row.
        display_details():
            Displays the values of each static variable of the Station class.
        update_status():
            Updates the status of the Station based on number of bikes
            available
    """

    def __init__(self, row: pd.Series = None, index: int = None) -> None:
        """
        Constructs an object of Station Class by creating corresponding
        static variables and performing certain methods based on value of row

            Parameters:
                row : pd.Series
                    Each row of the dataset is a station (default = None)
                index : int
                    Index of the row (default = None)

            Returns:
                None
        """
        self.id = None
        self.name = None
        self.address = None
        self.docks = None
        self.bikes_available = None
        self.status = None
        self.distance_ref = None
        self.zipcode = None
        self.pluscode = None

        if row is not None:
            self.dataset_row = row
            self.dataset_row_index = index
            self.update_static_variables()

    def generate_series_axes(self) -> list:
        """
        Returns names of attributes in row.

            Parameters:
                None

            Returns:
                self.dataset_row.axes : list
                    A list containing names of all attributes in a dataset row.
        """
        return self.dataset_row.axes

    def update_static_variables(self) -> None:
        """
        Updates the static variables of the class based on details
        from dataset row.

            Parameters:
                None

            Returns:
                None
        """
        self.id = int(self.dataset_row['Station ID'])
        self.name = self.dataset_row['Station Name']
        self.address = self.dataset_row['Address']
        self.zipcode = self.dataset_row['Zipcode']
        self.pluscode = self.dataset_row['Station Plus-Codes']
        self.distance_ref = self.dataset_row[' Distance from Base (TBH)']
        self.docks = int(self.dataset_row['Total Docks'])
        self.bikes_available = int(self.dataset_row['Bikes Available'])
        self.status = self.dataset_row['Station Status']

    def display_details(self) -> None:
        """
        Displays the values of each static variable of the Station class.

            Parameters:
                None

            Returns:
                None
        """
        print('\n\nStation ID:', self.id)
        print('Station Name:', self.name)
        print('Station Address:', self.address)
        print('Zipcode:', self.zipcode)
        print('Station Pluscode:', self.pluscode)
        print('Distance from base:', self.distance_ref)
        print('Total Docks at Station:', self.docks)
        print('Bikes Available at Station:', self.bikes_available)
        print('Status of Station:', self.status)
