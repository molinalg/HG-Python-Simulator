from modules.participant import Participant

# Class to represent districts
class District:

    def __init__(self,number):
        # Each district needs a number and 2 participants
        self.number = number
        self.members = [Participant("Name1",number), Participant("Name2",number)]
    
    def update_names(self,name1,name2):
        """The names of the participants can be updated"""
        self.members[0].name = name1
        self.members[1].name = name2