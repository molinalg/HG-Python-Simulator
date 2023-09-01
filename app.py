import tkinter as tk
from district import District
from participant import Participant

class App:
    window = None
    frames = []
    districts = []
    reorder = 0

    def __init__(self):
        # Window creation
        self.window = tk.Tk()
        self.window.title("Welcome to the Hunger Games")

        # ------------------------------ Welcome Page ------------------------------

        # Title label
        self.title_label = tk.Label(self.window, text="Hunger Games", font=("Helvetica", 24))
        self.title_label.pack(pady=20)

        # Play button
        self.play_button = tk.Button(self.window, text="Play", command=self.play)
        self.play_button.pack()

        # Exit button
        self.exit_button = tk.Button(self.window, text="Exit", command=self.window.destroy)
        self.exit_button.pack()

        # ------------------------------ Match Configuration Page ------------------------------

        # Add district button
        self.add_district_button = tk.Button(self.window, text="Add District", command=self.add_district)
    
    def start(self):
        self.window.mainloop()
    
    # # ------------------------------ Actions of the buttons ------------------------------
    def play(self):
        # Change from one screen to another
        self.play_button.destroy()
        self.exit_button.destroy()
        self.title_label.config(text="Match configuration", font=("Helvetica", 24))
        self.add_district_button.pack()

        # District data reset
        for label in self.frames:
            label.destroy()

    def add_district(self):
        if len(self.districts) < 12:
            # Asign the number of the district
            district_number = 1
            for district in self.districts:
                if district.number > district_number:
                    break
                district_number += 1

            # Container for the districts previews
            district_frame = tk.Frame(self.window)
            district_frame.pack()

            tk.Label(district_frame, text="District " + str(district_number)).pack(side=tk.LEFT, padx=10, pady=5)

            # Creation of a new district
            tk.Label(district_frame, text="Name1").pack(side=tk.LEFT, padx=10, pady=5)
            tk.Label(district_frame, text="Name2").pack(side=tk.LEFT, padx=10, pady=5)

            edit_button = tk.Button(district_frame, text="Edit", command=lambda dist_num=district_number: self.edit_district(dist_num))
            edit_button.pack(side=tk.LEFT, padx=10, pady=5)

            remove_button = tk.Button(district_frame, text="Remove", command=lambda dist_num=district_number: self.remove_district(dist_num))
            remove_button.pack(side=tk.LEFT, padx=10, pady=5)

            self.frames.append(district_frame)
            self.districts.append(District(district_number))

            if self.reorder != 0:
                # Sorting the list of districts
                self.districts.sort(key=lambda x: x.number)
                # Sorting the list of frames
                self.frames.sort(key=lambda x: int(x.winfo_children()[0].cget("text").split(" ")[1]))
                # Order the view of the frames
                for frame in self.frames:
                    frame.pack_forget()
                for frame in self.frames:
                    frame.pack()
                
                self.reorder -= 1
        
        # Check if the max of 12 districts is reached
        if len(self.districts) == 12:
            self.add_district_button.config(state=tk.DISABLED)
    
    def edit_district(self,district_number):
        # Create a new window
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Edit District " + str(district_number))

        # Container for the districts previews
        district_frame = tk.Frame(edit_window)
        district_frame.pack()

        # Names of the district in editable text fields
        name1 = tk.Entry(district_frame)
        name2 = tk.Entry(district_frame)
        for district in self.districts:
            if district.number == district_number:
                name1_text = district.members[0].name
                name2_text = district.members[1].name
                name1.insert(0, name1_text)
                name2.insert(0, name2_text)
                break
        name1.pack(side=tk.LEFT, padx=10, pady=5)
        name2.pack(side=tk.LEFT, padx=10, pady=5)

        # Save button
        save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_district(district_number,name1.get(),name2.get(),edit_window))
        save_button.pack(side=tk.LEFT, padx=10, pady=5)

    def save_district(self,district_number,name1_entry,name2_entry,edit_window):
        # Change the names of the participants
        print("Antes")
        for district in self.districts:
            print(district.members[0].name)
            print(district.members[1].name)
        for district in self.districts:
            if district.number == district_number:
                district.update_names(name1_entry,name2_entry)
                break
        # Change the names of the labels
        print("Entre medias")
        for district in self.districts:
            print(district.members[0].name + " " + str(district.number))
            print(district.members[1].name + " " + str(district.number))
        for frame in self.frames:
            if int(frame.winfo_children()[0].cget("text").split(" ")[1]) == district_number:
                frame.winfo_children()[1].config(text=name1_entry)
                frame.winfo_children()[2].config(text=name2_entry)
                break
        # Close the window
        edit_window.destroy()

    def remove_district(self,district_number):
        # Destroy and remove corresponding frame
        for frame in self.frames:
            if int(frame.winfo_children()[0].cget("text").split(" ")[1]) == district_number:
                frame.destroy()
                self.frames.remove(frame)
                break
        # Remove district from list
        for district in self.districts:
            if district.number == district_number:
                self.districts.remove(district)
                break
        # Sorting the list of districts
        self.districts.sort(key=lambda x: x.number)

        # Activate add district button if the max of 12 districts is not reached
        if len(self.districts) < 12:
            self.add_district_button.config(state=tk.NORMAL)
        
        self.reorder += 1