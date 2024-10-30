import tkinter as tk
from modules.district import District
from modules.game import Game

# Class to control the interface and the flow of the game
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

        # Dead tributes
        self.dead = []
    
    def start(self):
        """Open the window"""
        self.window.mainloop()

    def clean_window(self):
        """Clean a window"""
        for widget in self.window.winfo_children():
            widget.destroy()

    def menu(self):
        """Create the itinial menu"""
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
    
    def match_configuration(self):
        """Create the configuration page"""
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
        self.start_button.config(state=tk.DISABLED)

        # District data reset
        for label in self.frames:
            label.destroy()

    def add_district(self):
        """Add a district to the list of districts participating"""
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
        
        # Activate the start button if this is the first district added
        if len(self.districts) == 1:
            self.start_button.config(state=tk.NORMAL)
    
    def edit_district(self,district_number):
        """Edit the participants of a specific district"""
        # Create a new window
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Edit District " + str(district_number))

        # No fullscreen allowed for this window
        edit_window.attributes('-fullscreen', False)

        # Container for the window contents
        edit_frame = tk.Frame(edit_window)
        edit_frame.pack()

        # Container for the districts previews
        district_frame = tk.Frame(edit_frame)
        district_frame.pack()

        # Names of the district in editable text fields and buttons to edit their attributes
        name1 = tk.Entry(district_frame)
        attributes_button1 = tk.Button(district_frame, text="Attributes", command=lambda: self.change_attributes(edit_window,district_number,name1.get(),0))
        name2 = tk.Entry(district_frame)
        attributes_button2 = tk.Button(district_frame, text="Attributes", command=lambda: self.change_attributes(edit_window,district_number,name2.get(),1))

        for district in self.districts:
            if district.number == district_number:
                name1_text = district.members[0].name
                name2_text = district.members[1].name
                name1.insert(0, name1_text)
                name2.insert(0, name2_text)
                break
        name1.pack(side=tk.LEFT, padx=10, pady=5)
        attributes_button1.pack(side=tk.LEFT, padx=10, pady=5)
        name2.pack(side=tk.LEFT, padx=10, pady=5)
        attributes_button2.pack(side=tk.LEFT, padx=10, pady=5)

        # Save button
        save_button = tk.Button(edit_frame, text="Save", command=lambda: self.save_district(district_number,name1.get(),name2.get(),edit_window))
        save_button.pack(side=tk.LEFT, padx=10, pady=5)
    
    def change_attributes(self,window,district_number,name,index):
        """Change the attributes of a tribute"""
        # Obtain the tribute
        for district in self.districts:
            if district.number == district_number:
                member = district.members[index]

        # Create a new window
        attributes_window = tk.Toplevel(window)
        attributes_window.title("Edit Attributes: " + name)

        # Title label        
        title_label = tk.Label(attributes_window, text=name, font=("Helvetica", 15))
        title_label.pack(pady=20)

        # General
        attributes_frame = tk.Frame(attributes_window)
        attributes_frame.pack()

        # Variables to change the labels' text
        resistance_text = tk.StringVar()
        resistance_text.set("Resistance: {}/10".format(member.attributes["Resistance"]))
        strength_text = tk.StringVar()
        strength_text.set("Strength: {}/10".format(member.attributes["Strength"]))
        skills_text = tk.StringVar()
        skills_text.set("Skills: {}/10".format(member.attributes["Skills"]))
        luck_text = tk.StringVar()
        luck_text.set("Luck: {}/10".format(member.attributes["Luck"]))
        charisma_text = tk.StringVar()
        charisma_text.set("Charisma: {}/10".format(member.attributes["Charisma"]))

        # Attributes list and variables
        attributes = {"Resistance":resistance_text, "Strength":strength_text, "Skills":skills_text, "Luck":luck_text, "Charisma":charisma_text}

        # Variable to count the total amount of points left
        points = 20
        for total in attributes.values():
            points -= int(total.get().split(" ")[1][:-3])

        # Frame for the label with the points left
        points_frame = tk.Frame(attributes_frame)
        points_frame.pack()

        # Label to show the points left
        points_label_text = tk.StringVar()
        points_label_text.set("Points left: " + str(points))

        points_label = tk.Label(points_frame, textvariable=points_label_text)
        points_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        for attribute in attributes.keys():
            # Frame for each attribute
            attribute_frame = tk.Frame(attributes_frame)
            attribute_frame.pack()
            # Label for each attribute
            att_label = tk.Label(attribute_frame, textvariable=attributes[attribute])
            att_label.pack(side=tk.LEFT, padx=10, pady=5)
            # Buttons for each attribute
            minus_button = tk.Button(attribute_frame, text="-", command=lambda attr=attribute: self.decrease_value(attributes, attr, points, points_label_text))
            minus_button.pack(side=tk.LEFT)
            plus_button = tk.Button(attribute_frame, text="+", command=lambda attr=attribute: self.increase_value(attributes, attr, points, points_label_text))
            plus_button.pack(side=tk.LEFT)
        
        # Frame for the save button
        button_frame = tk.Frame(attributes_frame)
        button_frame.pack()

        # Save button
        save_attr_button = tk.Button(button_frame, text="Save", command=lambda: self.save_attributes(attributes, member, attributes_window))
        save_attr_button.pack(side=tk.LEFT)

    def increase_value(self,attributes,name,points,points_label_text):
        """Increase the label value for an attribute"""
        points = 20
        for total in attributes.values():
            points -= int(total.get().split(" ")[1][:-3])
        text = attributes[name].get()
        parts = text.split(" ")
        value = int(parts[1][:-3])
        if value >= 10 or points <= 0:
            return
        value += 1
        points -= 1
        points_label_text.set("Points left: " + str(points))
        attributes[name].set(parts[0]+" {}/10".format(value))

    def decrease_value(self,attributes,name,points,points_label_text):
        """Decrease the label value for an attribute"""
        points = 20
        for total in attributes.values():
            points -= int(total.get().split(" ")[1][:-3])
        text = attributes[name].get()
        parts = text.split(" ")
        value = int(parts[1][:-3])
        if value <= 0:
            return
        value -= 1
        points += 1
        points_label_text.set("Points left: " + str(points))
        attributes[name].set(parts[0]+" {}/10".format(value))
    
    def save_attributes(self,attributes,tribute,window):
        """Save the attributes of a tribute"""
        # Obtain the district number
        district_number = tribute.district
        # Load values into the dictionary
        final_attributes = {"Resistance":0,"Strength":0,"Skills":0,"Luck":0,"Charisma":0}
        final_attributes["Resistance"] = int(attributes["Resistance"].get().split(" ")[1][:-3])
        final_attributes["Strength"] = int(attributes["Strength"].get().split(" ")[1][:-3])
        final_attributes["Skills"] = int(attributes["Skills"].get().split(" ")[1][:-3])
        final_attributes["Luck"] = int(attributes["Luck"].get().split(" ")[1][:-3])
        final_attributes["Charisma"] = int(attributes["Charisma"].get().split(" ")[1][:-3])
        tribute.attributes = final_attributes

        # Find the tribute in the list of districts and update it
        for district in self.districts:
            if district.number == district_number:
                for member in district.members:
                    if member.name == tribute.name:
                        member.attributes = tribute.attributes
        
        # Close the window
        window.destroy()

    def save_district(self,district_number,name1_entry,name2_entry,window):
        """Save the changes of the district"""
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
        window.destroy()

    def remove_district(self,district_number):
        """Remove a district from the list of participating districts"""
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
        
        # Deactivate the atart button if there if there are no districts left
        if len(self.districts) == 0:
            self.start_button.config(state=tk.DISABLED)
        
        self.reorder += 1
    
    def match_screen(self):
        """Generate the match screen, starting the game"""
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
        dead = []
        self.events, self.tributes, dead = game.start_day1()

        for tribute in dead:
            self.dead.append(tribute)

        # Advance the first day
        self.advance_day(day,game)

        # Button to advance the day
        self.advance_button = tk.Button(self.window, text="Next", command=lambda: self.advance_day(day,game))
        self.advance_button.pack()

        # Set mode as 1 (regular day/night)
        self.mode = 1

    def advance_day(self,day,game):
        """Start the following day or night"""
        # Make sure there are still 2 or more tributes left
        if len(self.tributes) > 1:
            # Clean the events text
            self.events_text.config(state="normal")
            self.events_text.delete(1.0, tk.END)

            # Mode 0 means it is the cornucopia day, 1 is used for the rest
            if self.mode == 1:
                # Update to the current day/night/summary
                current_day = str(day.get())
                if str(day.get())[:3] == "Day":
                    day.set("Night " + current_day[4:])
                elif str(day.get())[:5] == "Night":
                    day.set("Summary Day " + current_day[6:])
                    # Display the tributes that died during the last day and night
                    self.events_text.insert(tk.END, "{num} gunshots in day {day}.\n\n".format(num=len(self.dead), day=current_day[6:0]), "center")
                    for tribute in self.dead:
                        self.events_text.insert(tk.END, "District {district}: {name}.\n\n".format(district=tribute["district"], name=tribute["name"]), "center")
                    self.dead = []
                    # Update the day label
                    self.day_label.config(text=day.get())
                    return
                else:
                    day.set("Day " + str(int(current_day[12:]) + 1))
    
                # Update the day label
                self.day_label.config(text=day.get())

                # Generate the events only if more than 1 tribute left
                dead = []
                self.events, self.tributes, dead = game.start_period()

                for tribute in dead:
                    self.dead.append(tribute)

            else:
                self.events_text.insert(tk.END, "It's the beginning of the Hunger Games. The horn sounds marking the start of the bloodbath.\n\n", "center")
                self.events_text.insert(tk.END, "The center of the arena, the Cornucopia, is full of valuable resources.\n\n", "center")

            # Update the events text
            for event in self.events:
                self.events_text.insert(tk.END, event + "\n\n", "center")
            
            self.events_text.config(state="disabled")

        else:
            # If there is less than 2 tributes left, the game is over
            self.finish_game()

    def finish_game(self):
        """Create the game over screen to show the winner"""
        # Clean the window
        self.clean_window()

        # Set the window title
        self.window.title("Game Over - Hunger Games")

        # Set the size of the window
        self.window.geometry("1000x600")

        # Title label for game over
        self.game_over_label = tk.Label(self.window, text="Game Over", font=("Helvetica", 22))
        self.game_over_label.pack(pady=20)
        
        # Check if there is 1 or 0 left:
        if len(self.tributes) == 1:
            # Winner announcement label
            self.winner_label = tk.Label(self.window, text="The Hunger Games come to an end! \n\n{name} from District {district} is the winner!".format(name=self.tributes[0]["name"],district=self.tributes[0]["district"]), font=("Helvetica", 12))
            self.winner_label.pack(pady=10)
        else:
            # No winner announcement label
            self.winner_label = tk.Label(self.window, text="The Hunger Games come to an end! \n\nThe arena is absolute chaos, everyone is dead!", font=("Helvetica", 12))
            self.winner_label.pack(pady=10)

        # Exit button
        self.exit_button = tk.Button(self.window, text="Exit", command=self.window.destroy)
        self.exit_button.pack(pady=10)
