from participant import Participant

class District:

    def __init__(self,number):
        self.number = number
        self.members = [Participant("Name1",number), Participant("Name2",number)]
    
    def update_names(self,name1,name2):
        self.members[0].name = name1
        self.members[1].name = name2