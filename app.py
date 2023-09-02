import tkinter as tk
from district import District
from game import Game

class App:
    window = None
    frames = []
    districts = []
    reorder = 0

    def __init__(self):
        # Window creation
        self.window = tk.Tk()

        # Menu creation
        self.menu()
    
    # Start the window
    def start(self):
        self.window.mainloop()

    # Clean the window
    def clean_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # Create the menu (welcome page)
    def menu(self):
        # Clean the window
        self.clean_window()

        # Title
        self.window.title("Welcome to the Hunger Games")

        # Title label
        self.title_label = tk.Label(self.window, text="Hunger Games", font=("Helvetica", 24))
        self.title_label.pack(pady=20)

        # Play button
        self.play_button = tk.Button(self.window, text="Play", command=self.match_configuration)
        self.play_button.pack()

        # Exit button
        self.exit_button = tk.Button(self.window, text="Exit", command=self.window.destroy)
        self.exit_button.pack()
    
    # Create the configuration page
    def match_configuration(self):
        # Clean the window
        self.clean_window()

        # Title
        self.window.title("Match configuration")

        # Title label        
        self.title_label = tk.Label(self.window, text="Match configuration", font=("Helvetica", 24))
        self.title_label.pack(pady=20)

        # Add district button
        self.add_district_button = tk.Button(self.window, text="Add District", command=self.add_district)
        self.add_district_button.pack()

        # Start match button
        self.start_button = tk.Button(self.window, text="Start Games", command=self.match_screen)
        self.start_button.pack()

        # District data reset
        for label in self.frames:
            label.destroy()

    # Add a district
    def add_district(self):
        # Current maximum of districts is 12
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

            # Edit button
            edit_button = tk.Button(district_frame, text="Edit", command=lambda dist_num=district_number: self.edit_district(dist_num))
            edit_button.pack(side=tk.LEFT, padx=10, pady=5)

            # Remove button
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
    
    # Edit a district participants
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

    # Save the changes of the district
    def save_district(self,district_number,name1_entry,name2_entry,edit_window):
        # Change the names of the participants
        for district in self.districts:
            if district.number == district_number:
                district.update_names(name1_entry,name2_entry)
                break
        
        # Change the names of the labels
        for frame in self.frames:
            if int(frame.winfo_children()[0].cget("text").split(" ")[1]) == district_number:
                frame.winfo_children()[1].config(text=name1_entry)
                frame.winfo_children()[2].config(text=name2_entry)
                break
        # Close the window
        edit_window.destroy()

    # Remove a district
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
    
    # Match screen
    def match_screen(self):
        # Clean the window
        self.clean_window()

        # Title
        self.window.title("Hunger Games")

        # Day label
        self.day_label = tk.Label(self.window, text="Day 1", font=("Helvetica", 24))
        self.day_label.pack(pady=20)

        # Variable to store the day number
        day = tk.StringVar()
        day.set("Day 1")

        # Text to show the events
        self.events_text = tk.Text(self.window, height=30, width=100, font=("Helvetica", 12))
        self.events_text.tag_configure("center", justify="center")
        self.events_text.config(state="disabled")
        self.events_text.pack()

        # Set mode as 0 (cornucopia day)
        self.mode = 0

        # Create a new game
        game = Game(self.districts)

        # Start the first day
        self.events = game.start_day1()

        # Advance the first day
        self.advance_day(day)

        # Button to advance the day
        self.advance_button = tk.Button(self.window, text="Next", command=lambda: self.advance_day(day))
        self.advance_button.pack()

    def advance_day(self,day):
        # Clean the events text
        self.events_text.config(state="normal")
        self.events_text.delete(1.0, tk.END)


        # Mode 0 means it is the cornucopia day, 1 is used for the rest
        if self.mode == 1:
            # Update to the current day/night/summary
            current_day = day.get()
            if day[:3] == "Day":
                day.set("Night " + current_day[4:])
            elif day[:5] == "Night":
                day.set("Summary Day " + current_day[6:])
            else:
                day.set("Day " + str(int(current_day[12:]) + 1))
            
            # Update the day label
            self.day_label.config(text=day.get())

        else:
            self.events_text.insert(tk.END, "It's the beginning of the Hunger Games. The horn sounds marking the start of the bloodbath.\n\n", "center")
            self.events_text.insert(tk.END, "The center of the arena, the Cornucopia, is full of valuable resources.\n\n", "center")

        # Update the events text
        for event in self.events:
            print(event)
            self.events_text.insert(tk.END, event + "\n\n", "center")
        
        self.events_text.config(state="disabled")
