# first step is to import all libraries

# import pandas to manipulate data frame
import pandas as pd

# this is to make it read in Jupyter Notebook
# add the following line back in if reading in Jupyter Notebook
# %matplotlib inline  

# import matplotlib and numpy in order to do heat map
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors

# import the appJar library for web application GUI check boxes
from appJar import gui

# This class takes the .csv file and formats that dataframes for use in making the chart

class Data_Processing:
    
    def __init__(self, file_name):
    
        # importing the eco-patch plants dataframe, with specific columns that I will be using
        self.df = pd.read_csv(file_name, usecols = ["Current Botanical Name", "Deciduous / Evergreen", "Flowers", "Flower RGB Color", "Flowering Season"]) 
        '''  
        This drops all rows that are missing any column of information from the selected columns. 
        In order to get this to work, it required going back to the data file to fill in information where there were blanks.
        Otherwise, rows of plants that I wanted to keep were removed.
        In most cases, I had to fill in flowering season information where there was none.
        For that, I referenced the CalFlora website.

        '''
        self.df.dropna(inplace=True)  
        
        # This sorts the dataframe alphabetically by 'Current Botanical Name'
        self.df.sort_values(by=['Current Botanical Name'], inplace=True)

        # This applies the seasons to list function to the flowering season data frame
        self.df["Flowering Season"] = self.df["Flowering Season"].apply(self.seasons_to_list)
        
        self.df["Flowering Season"]= self.df["Flowering Season"].apply(self.season_to_months)       
        
    def get_data(self):
        
        return self.df

    # This function converts a string to a list of strings split at the commas
    def seasons_to_list(self, season_string):
        
        return season_string.split(",")
    
    # This function turns a season into three distinct months and replaces the list of seasons in the flowering season column
    def season_to_months(self,season_list):
        
        # this is an empty list of months to be populated by the following function
        months = []
        for value in season_list:
            if value.upper() == "WINTER":
                months = months +["December", "January", "February"]
            if value.upper() == "SPRING":
                months = months +["March", "April", "May"]
            if value.upper() == "SUMMER":
                months = months +["June", "July", "August"]
            if value.upper()== "FALL":
                months = months +["September", "October", "November"]
            else:
                """
                if it's not a season then it must be a month, 
                in which case it should return the month
                """
                months = months + [value]  

        return months

# This class generates a new chart object using a data frame and a selected plant list

class Chart_Generator:
    
    def __init__(self, df, selected_plants):

        self.df = df
        # this defines the months that need to be looped through for each plant on the list and are the x-axis labels
        self.months = 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
        self.selected_plants = selected_plants
        """
        These functions use the Flower RGB Color column to create a list of RGB colors
        """
        """
        the first step is creating a mask to remove the dashes in the Flower RGB Color Column, 
        there are currently a lot of dashes for placeholders since I haven't assigned an RGB color for every plant yet
        """
        # This defines the color to print when a plant is evergreen but not flowering
        self.green = '#C9D589'
        # This defines the color to print when a plant is not flowering and is not deciduous
        self.white = '#FFFFFF'

        colors_mask = df["Flower RGB Color"] != '-'
        # The mask is applied to the Flower RGB Color column
        self.colors = df["Flower RGB Color"][colors_mask]
        # here I append the data frame list with white (no flowers and not evergreen) and green (no flowers but evergreen plant)
        self.colors = self.colors.append(pd.Series([self.white, self.green]))
        # I only want unique RGB colors from the list
        self.colors = self.colors.unique()
        """
        This creates a dictionary that maps RGB colors to an index number 
        where arange(1,len(colors)+1) reindexes the plants because the addition of white and green
        resulted in duplicate index numbers
        """
        self.color_to_index = dict(zip(self.colors,np.arange(1,len(self.colors)+1)))
        
        # Run the selected plants through the build_chart_data function to create chart_data, which is the list of lists with the color by index colors
        self.chart_data = self.build_chart_data()

    # this function converts a month to a color
    def month_to_color(self, df, name, month):
        
        plant_row = df[df["Current Botanical Name"]== name]
        flowering_months = plant_row["Flowering Season"]
        if month in flowering_months.values[0]:
            return plant_row["Flower RGB Color"].values[0] 
        elif plant_row["Deciduous / Evergreen"].values[0] == "Evergreen":
            return self.green
        else:
            return self.white   
    
    #this returns the array of color indicies by loop through selected plants
    def build_chart_data(self):
        
        # chart_color list is initalized to an empty list
        chart_colors= []
        print(self.color_to_index)
        for plant_name in self.selected_plants:
            # plant colors per month is initalized to an empty list- a new list is created for each plant
            plant_colors_per_month=[]
            # this is a nested loop that creates a list for each plant within the chart_colors list
            for month in self.months:
                # for each month, the month_to_color function is run to get the plant color for that month
                plant_color = self.month_to_color(self.df, plant_name, month)
                plant_colors_per_month = plant_colors_per_month +  [self.color_to_index[plant_color]]
            # the plant_colors_per_month list is added to the chart_colors list
            chart_colors = chart_colors + [plant_colors_per_month]  
        # after looping through all months for all plants, the function returns the chart_colors list of lists
        return chart_colors
        
    def print_chart(self):
        
        """
        The following code is adapted from the MatPlotLib documentation on annotated heat maps, which map a color to a number:
        https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html#sphx-glr-gallery-images-contours-and-fields-image-annotated-heatmap-py

        """

        # Define colormap from 1,2,3,... to colors
        cmap = matplotlib.colors.ListedColormap(self.colors)
        f = plt.figure()
        ax = plt.gca()
        ax.invert_yaxis()
        ax.imshow(self.chart_data, cmap=cmap, aspect="auto", clim = (1,len(self.colors)))
        ax.set_xticks(np.arange(len(self.months)))
        # This sets the ticks to the length of the selected plant list
        ax.set_yticks(np.arange(len(self.selected_plants)))
        # This sets the x axis labels to the months (defined previously)
        ax.set_xticklabels(self.months, fontsize=8)
        # This sets the y axis labels to the selected_plants list
        ax.set_yticklabels(self.selected_plants, fontsize=8)
        # This sets the title for the chart
        ax.set_title("Plant Colors in Year")
        # This formats the labels to read along the x axis
        plt.setp(ax.get_xticklabels(), rotation=-30, ha="left",
                     rotation_mode="anchor")
        # the following turns the edges of the axis off
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        # the following makes the text more condensed so it fits
        plt.tight_layout()
        # the following is needed to get the chart to show correctly when using Jupyter notebook
        plt.show()

"""
This is the user class, 
which is able to select plants from the all_plants list, 
using the appJar checkbox GUI: http://appjar.info/.
Selected plants are added to a selected plants list

"""
class User:
    
    def __init__(self, username, password):
        
        self.username = username
        self.password = password
        # initiating an empty list for selected plants
        self.selected_plants = []
    
    def select_plants(self, all_plants):

        # create a GUI variable called app
        app = gui()
        # rows and columns are defined to get two columns split halfway through the total number rows
        row = 0
        column = 0
        max_rows = round(len(all_plants)/3.0)+1
        # looping through the plants in the all plants list 
        for plant in all_plants:
            # creating a check box for each plant as it loops
            app.addCheckBox(plant, row, column)
            """
            this makes the check boxes pre-ticked if the plant has been previously selected 
            so that user can't reselect the same plant multiple times
            """
            if plant in self.selected_plants:
                app.setCheckBox(plant, ticked = True, callFunction = False)
            # this adds a new column once the row is more than or equal to half the total number of rows
            row = row + 1
            if row >= max_rows:
                column = column + 1
                row = 0 
        # this creates the done button at the bottom of the pop up window gui    
        app.addButton ("Done", app.stop, max_rows+1, 2)
        # running checkbox GUI in a new pop-up window   
        app.go()
        # creating a new variable to capture the dictionary of plants and corresponding True/ False values
        checkbox_response = (app.getAllCheckBoxes())
        #looping through plants in checkbox_response
        self.selected_plants = []
        for plant in checkbox_response:
            # if the value of the plant is True then it gets added 
            # to the list of selected plants
            if checkbox_response[plant] == True:
                # this line adds the plant to the selected plant list
                self.selected_plants= self.selected_plants + [plant] 
    
    # this method returns the selected plant list
    def get_plants(self):
        
        return self.selected_plants

# the web application object simulates a website interaction with the program
class Web_Application:
     
    def __init__(self):
        
        # this is a dictionary that stores users and user information and is a private variable
        self.__users = {} 
        self.data = Data_Processing("Eco_Patch_Plants_Dataset.csv")
        self.df_months = self.data.get_data()
        self.all_plants = self.df_months["Current Botanical Name"].values
    
    # this method uses the Chart Generator class 
    def make_chart(self, user): 
        
        selected_plants = user.get_plants()
        if selected_plants == []:
            print("You have no plants selected. Please select plants to make a chart.")
        else:
            chart = Chart_Generator(self.df_months, selected_plants)
            chart.print_chart()
    
    # this method prompts the user to login and offers a menu of options 
    def interface(self):
        
        # login_input loops back to "L" to bring users back to the login unless they press "Q" to quit
        login_input = "L"   
        while login_input == "L":
            login_input= input("Would you like to login? Press L. Would you like to quit? Press Q.")
            user = self.login()
            # define user_input as an empty string prior to using it
            user_input = ""
            # as long as the user_input is not 4 indicating "logout", the following menu is printed
            while user_input != "4":
                print("Which of the following would you like to do?")
                print("1. Review your plant list")
                print("2. Change your plant list")
                print("3. See a chart of your selected plants")
                print("4. Logout")
                user_input = input("Please enter your selection number: ")
                if user_input == "1":
                    print(user.get_plants())
                if user_input == "2":
                    # this causes the checkbox gui to pop up with the list of all_plants to select from
                    user.select_plants(self.all_plants)
                if user_input == "3":
                    # this uses the make_chart method defined in this class
                    self.make_chart(user)
                if user_input == "4":
                    print(f"Goodbye, {user.username}.")
            login_input= input("Would you like to login? Press L. Would you like to quit? Press Q.")

          
    # this method allows users to login to the web application     
    def login(self):
        
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = self.__users[username]
        # if the password matches then the user is welcomed
        if password == user.password:
            print(f"Welcome, {username}.")
            return user
        # if the password is incorrect then this happens
        else:
            print("Incorrect username or password")

    # this method accepts a username and a password argument and creates new user objects    
    def add_user(self, username, password):
        
        self.__users[username] = User(username, password)     

#this is the main method, which directs the flow of the program. 
def main():
    
    # Make the Web App
    web_app = Web_Application()

    # Add a user
    web_app.add_user("plant_lover1","achillea")
    
    # Start user interface
    web_app.interface()
    

if __name__ == "__main__":
    main()


