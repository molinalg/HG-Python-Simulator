# Class to represent tributes
class Participant:

    def __init__(self,name,district):
        # Each tribute has a name, a district and a set of attributes
        self.name = name
        self.district = district
        self.attributes = {"Resistance":0,"Strength":0,"Skills":0,"Luck":0,"Charisma":0}
    
    