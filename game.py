from graph_manager import Graph_Manager
from csv_management.csv_reader import CSV_Reader
class Game:

    def __init__(self, districts):
        # Create a graph manager
        self.graph_manager = Graph_Manager()

        # Read the csv files
        csv_reader = CSV_Reader('csv_management/day1-hg.csv')
        self.data_day1 = csv_reader.read()

        # Create a list of tributes
        self.tributes = self.generate_tributes(districts)
    
    # Create a list of tributes
    def generate_tributes(self, districts):
        tributes = []
        for district in districts:
            for member in district.members:
                tribute = {
                    "name": member.name,
                    "district": member.district,
                    "graph": self.graph_manager.create_graph(self.data_day1),
                    "inventory": [],
                    "status": "alive"
                }
                tributes.append(tribute)
        return tributes

    # Start day 1 of the game
    def start_day1(self):
        return self.graph_manager.obtain_actions(self.tributes, (('INITIAL', ''),))
