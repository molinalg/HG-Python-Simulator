import networkx as nx
import random
from csv_management.csv_reader import CSV_Reader
from matplotlib import pyplot as plt

class Graph_Manager:

    def __init__(self):
        pass
    
    def create_graph(self,data):
        # Creates a graph from the given data
        temp_graph = nx.DiGraph()
        for row in data:
            starting_node = tuple(row[0].items())
            target_node = tuple(row[1].items())
            weight = float(row[2])
            effect = row[3]

            if starting_node not in temp_graph:
                temp_graph.add_node(starting_node)
            if target_node not in temp_graph:
                temp_graph.add_node(target_node)

            temp_graph.add_edge(starting_node, target_node, weight=weight, effect=effect)
        
        return temp_graph
        
    def display_graph(self,graph):
        # Displays the given graph on screen
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10)
        plt.show()

    def obtain_actions(self,tributes,start_node):
        # List to store the actions
        actions = []
        while len(tributes) > 0:
            # Message with the action
            message = ""
            # Select a random tribute
            tribute = random.choice(tributes)
            tributes.remove(tribute)
            message += tribute["name"] + " from district " + str(tribute["district"]) + " "
            graph = tribute["graph"]
            
            # Find a final node
            action_message = self.find_final_nodes(graph,start_node)
            
            if "[Y]" in action_message:
                if len(tributes) == 0:
                    while "[Y]" not in action_message:
                        action_message = self.find_final_nodes(graph,start_node)
                else:
                    tribute2 = random.choice(tributes)
                    tributes.remove(tribute2)
                    # Add the new tribute to the message
                    action_message = action_message.replace("[Y]",tribute2["name"] + " from district " + str(tribute2["district"]))
            
            message += action_message

            actions.append(message)
        
        return actions

    def find_final_nodes(self,graph,start_node):
        # Find a final node in the graph and form the message to return
        message = ""
        curent_node = start_node
        while True:
            # Go to the next node
            next_node = self.next_node(graph, curent_node)

            # Check if the next node is a final node
            if next_node == None:
                break

            # Else repeat the process
            message += next_node[0][1]
            curent_node = next_node

        return message

    def next_node(self,graph, current_node):
        # Get the list of edges
        edges = graph.edges(current_node, data=True)

        if len(edges) == 0:
            return None

        # Get the possible next nodes and the weights
        possible_next_nodes = []
        weights = []
        for edge in edges:
            possible_next_nodes.append(edge[1])
            weights.append(edge[2]["weight"])

        # Choose a random next node
        next_node = random.choices(possible_next_nodes, weights=weights)[0]
        return next_node