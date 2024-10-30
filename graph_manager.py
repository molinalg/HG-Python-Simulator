import networkx as nx
import random
from matplotlib import pyplot as plt

# Class to manage graphs and events
class Graph_Manager:

    def __init__(self,objects,creatures):
        # Objects and animals in the game
        self.objects = objects
        self.creatures = creatures
    
    def create_graph(self,data):
        """Creates a graph from the given data"""
        temp_graph = nx.DiGraph()
        # Process each row
        for row in data:
            starting_node = tuple(row[0].items())
            target_node = tuple(row[1].items())
            weight = float(row[2])
            effect = row[3]
            
            # Add every node not already present
            if starting_node not in temp_graph:
                temp_graph.add_node(starting_node)
            if target_node not in temp_graph:
                temp_graph.add_node(target_node)

            temp_graph.add_edge(starting_node, target_node, weight=weight, effect=effect)

        return temp_graph
        
    def display_graph(self,graph):
        """Displays the given graph on screen"""
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10)
        plt.show()

    def obtain_actions_day1(self,tributes):
        """Obtains and processes the actions of the cornucopia day"""
        # List to store the actions
        actions = []
        # List to store tributes that have already participated
        processed = []
        # List to store the inventory and state changes
        changes = []

        while len(tributes) > 0:
            # Message with the action
            message = ""
            # Select a random tribute
            tribute = random.choice(tributes)
            tributes.remove(tribute)
            message += tribute["name"] + " from district " + str(tribute["district"]) + " "
            graph = tribute["graphs"][0]
            start_node = tribute["node"]

            # Find a final node
            action_message, result = self.find_final_nodes(graph,start_node)
            
            if "[Y]" in action_message:
                if len(tributes) == 0:
                    while "[Y]" in action_message:
                        action_message, result = self.find_final_nodes(graph,start_node)
                else:
                    tribute2 = random.choice(tributes)
                    tributes.remove(tribute2)
                    if result == "YO":
                        tribute2["status"] = "dead"
                    elif result == "HO":
                        tribute2["status"] = "injured"
                        changes.append([tribute2["name"],"I"])
                    processed.append(tribute2)
                    # Add the new tribute to the message
                    action_message = action_message.replace("[Y]",tribute2["name"] + " from district " + str(tribute2["district"]))
            
            message += action_message

            # Process if the tribute is injured or dead
            if result == "YT":
                tribute["status"] = "dead"
            elif result == "HT":
                tribute["status"] = "injured"
                changes.append([tribute["name"],"I"])

            # Choose a random object if it has appeared in the action
            if "[O]" in message:
                selected_object = random.choices(self.objects)[0]
                tribute["inventory"].append(selected_object)
                message = message.replace("[O]",selected_object[0])
                changes.append([tribute["name"],selected_object[1]])

            processed.append(tribute)
            actions.append(message)
        
        return actions, processed, changes

    def obtain_actions(self,tributes):
        """Obtains and processes a new set of events"""
        # List to store the actions
        actions = []
        # List to store tributes that have already participated
        processed = []
        # List to store the inventory and state changes
        changes = []

        current_node = None
        while len(tributes) > 0:
            # Message with the action
            message = ""
            # Select a random tribute
            tribute = random.choice(tributes)
            tributes.remove(tribute)
            message += tribute["name"] + " from district " + str(tribute["district"]) + " "
            graph = tribute["graphs"][1]
            current_node = tribute["node"]
            # Find the next node
            current_node, result = self.next_node(graph,current_node,current_node)

            if "[Y]" in current_node[0][1]:
                # If there is no other tribute to fight with, we select another node
                if len(tributes) == 0:
                    while "[Y]" in current_node[0][1]:
                        current_node, result = self.next_node(graph,tribute["node"],result)

                else:
                    message += current_node[0][1]
                    tribute2 = random.choice(tributes)
                    tributes.remove(tribute2)
                    # Add the new tribute to the message
                    message = message.replace("[Y]",tribute2["name"] + " from district " + str(tribute2["district"]))
                    # If there was a fight, we generate the result
                    if current_node == (('FIGHT', 'encounters [Y] and decides to fight, '),):
                        current_node, result = self.next_node(graph,current_node,result)

                        if result == "YO":
                            tribute2["status"] = "dead"
                        elif result == "HO":
                            tribute2["status"] = "injured"
                            changes.append([tribute2["name"],"I"])
                        processed.append(tribute2)

            # If a random event occurs, we select a random event from the list the tribute has using the weights
            if "[R]" in current_node[0][1]:
                # Get the list of random events
                random_events = tribute["random_events"]
                possible_events = []
                weights = []
                results = []
                for event in random_events:
                    possible_events.append(event[0])
                    weights.append(float(event[1]))
                    results.append(event[2])
                
                # Choose a random event
                event = random.choices(possible_events, weights=weights)[0]
                # Get the index of the event
                index = possible_events.index(event)
                # Get the result of the event
                result = results[index]
                # Get the message of the event
                message += event

            # If a random hidden event occurs, we select a random event from the list the tribute has using the weights
            elif "[RH]" in current_node[0][1]:
                # Get the list of random events
                random_events = tribute["random_hide_events"]
                possible_events = []
                weights = []
                results = []
                for event in random_events:
                    possible_events.append(event[0])
                    weights.append(float(event[1]))
                    results.append(event[2])
                
                # Choose a random event
                event = random.choices(possible_events, weights=weights)[0]
                # Get the index of the event
                index = possible_events.index(event)
                # Get the result of the event
                result = results[index]
                # Get the message of the event
                message += event

            else:
                message += current_node[0][1]

            tribute["node"] = current_node

            # Choose a random object if it has appeared in the action
            if "[O]" in message:
                selected_object = random.choices(self.objects)[0]
                tribute["inventory"].append(selected_object)
                message = message.replace("[O]",selected_object[0])
                changes.append([tribute["name"],selected_object[1]])
            
            # Choose a random gift if it has appeared in the action
            if "[G]" in message:
                selected_gift = random.choices(self.objects)[0]
                tribute["inventory"].append(selected_gift)
                message = message.replace("[G]",selected_gift[0])
                changes.append([tribute["name"],selected_gift[1]])

            # Choose a random creature if it has appeared in the action
            if "[A]" in message:
                selected_creature = random.choices(self.creatures)[0]
                message = message.replace("[A]",selected_creature[0])

            actions.append(message)

            # Process if the tribute is injured or dead
            if result == "YT":
                tribute["status"] = "dead"
            elif result == "HT":
                tribute["status"] = "injured"
                changes.append([tribute["name"],"I"])

            processed.append(tribute)

        return actions, processed, changes

    def find_final_nodes(self,graph,start_node):
        """Returns a final node in the graph"""
        # Find a final node in the graph and form the message to return
        message = ""
        current_node = start_node
        current_result = None
        while True:
            # Go to the next node
            next_node, result = self.next_node(graph, current_node,current_result)

            # Check if the next node is a final node
            if next_node == None:
                break

            # Else repeat the process
            message += next_node[0][1]
            current_node = next_node
            current_result = result

        return message, result

    def next_node(self,graph,current_node,current_result):
        """Returns the next node in the graph"""
        # Get the list of edges
        edges = graph.edges(current_node, data=True)

        if len(edges) == 0:
            return None, current_result

        # Get the possible next nodes, the weights and the results
        possible_next_nodes = []
        weights = []
        results = []
        for edge in edges:
            possible_next_nodes.append(edge[1])
            weights.append(edge[2]["weight"])
            results.append(edge[2]["effect"])

        # Choose a random next node
        next_node = random.choices(possible_next_nodes, weights=weights)[0]
        return next_node, results[possible_next_nodes.index(next_node)]