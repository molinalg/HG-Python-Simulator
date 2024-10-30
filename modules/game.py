from graph_manager import Graph_Manager
from csv_reader import CSV_Reader

# Class to execute and process events
class Game:

    def __init__(self, districts):
        # Read the csv files
        csv_reader = CSV_Reader()
        self.data_day1 = csv_reader.read('events/day1-hg.csv')
        self.data_general = csv_reader.read('events/general-hg.csv')
        self.random, self.random_resistance, self.random_survival, self.random_hide  = csv_reader.load_random()
        self.objects, self.creatures = csv_reader.load_utils()

        # Create a graph manager
        self.graph_manager = Graph_Manager(self.objects,self.creatures)

        # Create a list of tributes
        self.tributes = self.generate_tributes(districts)

        # Create a list for the dead
        self.dead = []
    
    def generate_tributes(self, districts):
        """Create a list of tributes"""
        tributes = []
        for district in districts:
            for member in district.members:
                # We need to adapt the probabilitites of certain events to the selected attributes
                # Resistance random events probability adaptations
                resistance_random = self.random_resistance
                for event in resistance_random:
                    event[1] = float(event[1]) * (1-member.attributes["Resistance"]/13)
                # Events affected by strength adaptation
                data_day1 = self.alter_probabilities(member,"Strength",self.data_day1,{'ATTACK': 'attacks [Y] '},[[0,"+"],[2,"+"]],[15,35])
                data_general = self.alter_probabilities(member,"Strength",self.data_general,{'FIGHT': 'encounters [Y] and decides to fight, '},[[0,"+"],[2,"+"]],[17,35])
                data_general = self.alter_probabilities(member,"Strength",data_general,{'INITIAL': ''},[[1,"+"]],[22])
                data_general = self.alter_probabilities(member,"Strength",data_general,{'RANDOM': '[R]'},[[0,"+"]],[22])
                # Events affected by skills adaptation
                data_day1 = self.alter_probabilities(member,"Skills",self.data_day1,{'INITIAL': ''},[[3,"+"]],[10])
                data_general = self.alter_probabilities(member,"Skills",data_general,{'SEARCH_RES': 'sets off in search of resources.'},[[3,"+"]],[20])
                data_general = self.alter_probabilities(member,"Skills",data_general,{'RANDOM': '[R]'},[[1,"+"],[3,"+"]],[20,20])
                survival_random = self.random_survival
                for event in survival_random:
                    event[1] = float(event[1]) * (1-member.attributes["Skills"]/15)
                hide_random = self.random_hide
                for event in hide_random:
                    event[1] = float(event[1]) * (1-member.attributes["Skills"]/15)
                # Events affected by charisma adaptation
                data_day1 = self.alter_probabilities(member,"Charisma",self.data_day1,{'CORNUCOPIA': 'runs to the Cornucopia. '},[[2,"-"]],[10])
                data_general = self.alter_probabilities(member,"Charisma",data_general,{'INITIAL': ''},[[3,"+"]],[23])
                data_general = self.alter_probabilities(member,"Charisma",data_general,{'RANDOM': '[R]'},[[5,"+"]],[23])
                data_general = self.alter_probabilities(member,"Charisma",data_general,{'SEARCH_TRIB': 'hunts for tributes.'},[[5,"+"]],[23])
                data_general = self.alter_probabilities(member,"Charisma",data_general,{'SEARCH_RES': 'sets off in search of resources.'},[[5,"+"]],[23])
                data_general = self.alter_probabilities(member,"Charisma",data_general,{'HIDE': 'hides from other tributes.'},[[3,"+"]],[23])
                data_general = self.alter_probabilities(member,"Charisma",data_general,{'FIGHT': 'encounters [Y] and decides to fight, '},[[1,"-"],[3,"+"]],[12,12])
                # Events affected by luck adaptation
                data_day1 = self.alter_probabilities(member,"Luck",self.data_day1,{'CORNUCOPIA': 'runs to the Cornucopia. '},[[0,"+"]],[10])
                data_general = self.alter_probabilities(member,"Luck",data_general,{'SEARCH_RES': 'sets off in search of resources.'},[[3,"+"]],[20])
                data_general = self.alter_probabilities(member,"Luck",data_general,{'RANDOM': '[R]'},[[3,"+"]],[20])
                data_general = self.alter_probabilities(member,"Luck",data_general,{'INITIAL': ''},[[5,"-"]],[15])
                data_general = self.alter_probabilities(member,"Luck",data_general,{'SEARCH_RES': 'sets off in search of resources.'},[[2,"-"]],[10])
                data_general = self.alter_probabilities(member,"Luck",data_general,{'RANDOM_HIDE': '[RH]'},[[6,"+"]],[30])
                for event in resistance_random:
                    event[1] = float(event[1]) * (1-member.attributes["Luck"]/25)
                for event in survival_random:
                    event[1] = float(event[1]) * (1-member.attributes["Luck"]/25)
                
                # Join the random events and balance them
                tribute_random = []
                for event in self.random:
                    tribute_random.append(event)
                for event in resistance_random:
                    tribute_random.append(event)
                for event in survival_random:
                    tribute_random.append(event)
                total = 0
                for event in tribute_random:
                    total += float(event[1])
                for event in tribute_random:
                    event[1] = str(float(event[1])/total)

                tribute = {
                    "name": member.name,
                    "district": member.district,
                    "graphs": [self.graph_manager.create_graph(data_day1), self.graph_manager.create_graph(data_general)],
                    "inventory": [],
                    "status": "alive",
                    "node": (('INITIAL', ''),),
                    "random_events": tribute_random,
                    "random_hide_events": hide_random,
                    "data": data_general
                }

                tributes.append(tribute)
                
        return tributes

    # Receives an affected node, a value to alter probability values and the indexes affected. Balances all after the increase
    def alter_probabilities(self,member,attribute,data,affected_node,indexes,values):
        """Alter the probabilities read in the csv for a specific person."""
        # List to store temporary probabilities
        edge_probs = []

        # We first collect all probabilities starting with the affected node
        for event in data:
            if event[0] == affected_node:
                edge_probs.append(float(event[2]))
        
        # Now we change the selected probabilities
        for index in indexes:
            if index[1] == "+":
                edge_probs[index[0]] += ((1-edge_probs[index[0]])*member.attributes[attribute]/values[0])
                values.pop(0)
            elif index[1] == "-":
                edge_probs[index[0]] = edge_probs[index[0]] * (1-member.attributes[attribute]/values[0])
                values.pop(0)

        return self.balance_data(edge_probs,data,affected_node)
    
    
    def alter_probabilities_match(self,data,affected_node,indexes):
        """Alter the probabilities in the middle of a match generating a new graph"""
        # List to store temporary probabilities
        edge_probs = []

        # We first collect all probabilities starting with the affected node
        for event in data:
            if event[0] == affected_node:
                edge_probs.append(float(event[2]))
        
        # Now we change the selected probabilities
        for index in indexes:
            if index[1] == "+":
                edge_probs[index[0]] += ((1-edge_probs[index[0]]) * 0.3)
            elif index[1] == "-":
                edge_probs[index[0]] -= edge_probs[index[0]] * 0.2

        return self.balance_data(edge_probs,data,affected_node)

    def balance_data(self, edge_probs, data, affected_node):
        """Balance the probabilities after altering them"""
        # Balance all of them
        total = 0
        for probability in edge_probs:
            total += probability
        
        counter = 0
        for probability in edge_probs:
            probability = probability/total
            edge_probs[counter] = probability
            counter += 1

        # Update probabilitites
        for event in data:
            if event[0] == affected_node:
                event[2] = str(edge_probs[0])
                edge_probs.pop(0)

        return data

    def start_day1(self):
        """Start cornucopia day"""
        actions, tributes, changes = self.graph_manager.obtain_actions_day1(self.tributes)
        alive = []
        for tribute in tributes:
            if tribute["status"] == "dead":
                self.dead.append(tribute)
            else:
                alive.append(self.process_changes(tribute, changes))
        self.tributes = alive
        return actions, self.tributes, self.dead

    def start_period(self):
        """Start a regular day or night"""
        self.dead = []
        actions, tributes, changes = self.graph_manager.obtain_actions(self.tributes)
        alive = []
        for tribute in tributes:
            if tribute["status"] == "dead":
                self.dead.append(tribute)
            else:
                alive.append(self.process_changes(tribute, changes))            
        self.tributes = alive
        return actions, self.tributes, self.dead


    def process_changes(self, tribute, changes):
        """Process any graph changes needed"""
        # Check if the probabilitites need to be altered
        altered = False
        for change in changes:
            if tribute["name"] == change[0]:
                # If the tribute has a new weapon
                if change[1] == "W":
                    data = tribute["data"]
                    new_data = self.alter_probabilities_match(data,{'FIGHT': 'encounters [Y] and decides to fight, '},[[0,"+"],[2,"+"]])
                    new_data = self.alter_probabilities_match(new_data,{'INITIAL': ''},[[1,"+"]])
                    new_data = self.alter_probabilities_match(new_data,{'RANDOM': '[R]'},[[0,"+"]])
                    altered = True
                # If the tribute has a new resource
                elif change[1] == "R":
                    data = tribute["data"]
                    new_data = self.alter_probabilities_match(data,{'FIGHT': 'encounters [Y] and decides to fight, '},[[0,"+"],[2,"+"]])
                    new_data = self.alter_probabilities_match(new_data,{'INITIAL': ''},[[1,"+"]])
                    new_data = self.alter_probabilities_match(data,{'HIDE': 'hides from other tributes.'},[[4,"+"]])
                    altered = True
                # If the tribute is injured
                elif change[1] == "I":
                    # Check if there is medicine in the inventory
                    found = False
                    for item in tribute["inventory"]:
                        if item[1] == "M":
                            tribute["inventory"].remove(item)
                            tribute["status"] = "alive"
                            found = True
                    # If he is still injured, alter the probabilities        
                    if not found:
                        data = tribute["data"]
                        new_data = self.alter_probabilities_match(data,{'FIGHT': 'encounters [Y] and decides to fight, '},[[0,"-"],[2,"-"]])
                        new_data = self.alter_probabilities_match(new_data,{'INITIAL': ''},[[1,"-"]])
                        new_data = self.alter_probabilities_match(new_data,{'RANDOM': '[R]'},[[0,"-"]])
                        altered = True
                # If the tribute has medicine
                elif change[1] == "M":
                    if tribute["status"] == "injured":
                        tribute["status"] = "alive"
                        data = tribute["data"]
                        new_data = self.alter_probabilities_match(data,{'FIGHT': 'encounters [Y] and decides to fight, '},[[0,"+"],[2,"+"]])
                        new_data = self.alter_probabilities_match(new_data,{'INITIAL': ''},[[1,"+"]])
                        new_data = self.alter_probabilities_match(new_data,{'RANDOM': '[R]'},[[0,"+"]])
                        altered = True
                # If the probabilities have been altered, update the tribute's data and graph
                if altered:
                    tribute["data"] = new_data
                    tribute["graphs"][1] = self.graph_manager.create_graph(new_data)

        return tribute
