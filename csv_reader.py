import csv

# Class to load the CSV files
class CSV_Reader:

    def __init__(self):
        # Lists to store data
        self.data = []
        self.random = []
        self.random_resistance = []
        self.random_survival = []
        self.random_hide = []
        self.objects = []
        self.creatures = []
    
    def read(self,path):
        """Reads the content of a CSV file"""
        self.data = []
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.data.append(row)
            self.data.pop(0)
        csvfile.close()
        return self.parse_data()
    
    def parse_data(self):
        """Process the data read from a CSV file"""
        self.parsed_data = []
        for row in self.data:
            # Each row needs a specific final format
            temp_data = []
            temp_data.append({row[0]: row[1]})
            temp_data.append({row[2]: row[3]})
            temp_data.append(row[4])
            temp_data.append(row[5])
            self.parsed_data.append(temp_data)

        return self.parsed_data
    
    def load_random(self):
        """Read all the files of random events"""
        with open('random_events/random.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.random.append(row)
            self.random.pop(0)
        csvfile.close()

        with open('random_events/random_resistance.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.random_resistance.append(row)
            self.random_resistance.pop(0)
        csvfile.close()

        with open('random_events/random_survival.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.random_survival.append(row)
            self.random_survival.pop(0)
        csvfile.close()

        with open('random_events/random_hide.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.random_hide.append(row)
            self.random_hide.pop(0)
        csvfile.close()

        return self.random, self.random_resistance, self.random_survival, self.random_hide

    def load_utils(self):
        """Read the files with the objects and animals"""
        with open('miscellaneous/objects.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.objects.append(row)
            self.objects.pop(0)
        csvfile.close()

        with open('miscellaneous/creatures.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.creatures.append(row)
            self.creatures.pop(0)
        csvfile.close()

        return self.objects, self.creatures
