Hybrid Python Application and Data Visualization Project

![Plant Visually Demo](plant_visually.gif)

NOTE: to use application login with the username "plant_lover1" and the password "achillea". 
**NOTE: to use the application without creating a new user, login with the username "plant_lover1" and the password "achillea"**

## Introduction

This project is a hybrid python application and data science project in that it allows users to generate a visualization based on data from plants that they have selected. The plant data set comes from [Calscape](https://calscape.org/). This project is the same topic as my [Project 1](https://git.generalassemb.ly/hackerharker/Project01), and will even have similarly named classes but the classes will be programmed in a different way, additional classes are added, objects are created based on an external dataset, and instead of generating a chart by printing text, the data is used to produced a data visualization of select frames using MatPlotLib.

This project focuses on plants that are tolerant of or adapted to serpentine soils and that are native to the Potrero Hill Neighborhood in San Francisco. This tool is ultimately intended to go on a website as part of the [Eco-Patch](https://www.greenbenefit.org/project-blog/2020/7/10/7h2nn73s0ae13hhxm61nwnjdnvkkls) project, a larger effort to encourage people to plant plants that are native to the area and consequently have high habitat and biodiversity value. This tool is intended to get people engaged with and interested in these plants as well as help them figure out which combinations of plants they can plant so that they select a combination of plants that bloom in succession for year-round interest. This tool will help them visualize their plant list to make sure that they always have at least one plant from the list that has green foliage on any given month. The reason why I am focusing on this “bloom chart” visualization tool is because it is a function not already available on [Calscape](https://calscape.org/) and because I intend to use it myself in designing the planting plan for the test garden portion of the [Eco-Patch](https://www.greenbenefit.org/project-blog/2020/7/10/7h2nn73s0ae13hhxm61nwnjdnvkkls) project. For the test garden I am developing 8 different plant combinations with the goal that each has year round interest in the form of flowers or green foliage. My hope is that once I develop the tool I can deploy it to a website associated with this project so that individual homeowners and other landscape architects can use it. My hypothesis is that if people have access to a tool like this they will be more likely to plant plants that are native to the area. An additional outcome could be that I share this project with [Calscape](https://calscape.org/) so that they can add this functionality to their website.

## Data and Libraries

## Data Cleaning

## Summary of Classes

**Web_Application_Class**- simulates an interaction with a web application that allows users to login with a password (private variable), create a plant list, save their plant list, and create a visualization based on their plant list. This class can also accept new users. I intend on using [appJar](http://appjar.info/) to create a Boolean widget checkbox for plant selection. This web app interface will be text based and read as follows:
    
    User_login:

    User_password:

    Select_plants() # a function under the Web Application Class
Pop up box that lists all plants and allows you to select the ones you want to add to your plant list using the appJar checkbox

    Create_chart() # a function under the Chart Class
        Creates a chart based on the user selected plant list


User_Class- stores user profiles and their list of plants for the web app class.

Data_Processing_Class- This class will read in a .csv file from a plant database and use pandas to manipulate the dataframe as needed to create the chart. The data has been pulled from a website, Calscape, which aggregates data about native plants. I am specifically interested in the columns with the current botanical name, the plant type (annual or perennial), evergreen/deciduous, flowers (which indicates flower color), and flowering season. Interpolation will be necessary to format the data from the calscape dataset into a usable form so that users can create a chart from it. For example, the data lists the season that the plants are flowering but does not list by month, and so I will need a function to convert the season to specific months for the chart. Also if the plant is listed as being deciduous for a particular season then I will need a function to convert that information to show an empty bar on the chart for the months in that season. If the plant is listed as evergreen then I will want the bar on the chart to show as green when the plant is not flowering and showing a flower color on the chart.

Chart_Class- this class creates a bar chart visualization showing when what plant is blooming or displaying green foliage from a list of plants. The planting visualization will list the plants on the y axis and the months on the x axis. For each month the plants have a color. The color is the flower color if the plant is blooming, otherwise green if it is evergreen, and blank if it is deciduous, dormant for certain months, or an annual that has died back for the year. The chart will use the third party library, MatPlotLib. 

## Summary