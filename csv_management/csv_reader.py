import csv
class CSV_Reader:

    def __init__(self, path):
        self.path = path
        self.data = []
    
    def read(self):
        with open(self.path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                self.data.append(row)
            self.data.pop(0)
        return self.parse_data()
    
    def parse_data(self):
        self.parsed_data = []
        for row in self.data:
            temp_data = []
            temp_data.append({row[0]: row[1]})
            temp_data.append({row[2]: row[3]})
            temp_data.append(row[4])
            temp_data.append(row[5])
            self.parsed_data.append(temp_data)
        return self.parsed_data