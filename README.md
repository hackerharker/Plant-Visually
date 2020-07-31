# Plant Visually

![Plant Visually Demo](plant_visually.gif)

**NOTE: to use the application without creating a new user, login with the username "plant_lover1" and the password "achillea"**

## Summary

This project is a hybrid python application and data science project in that it allows users to generate a visualization based on data from plants that they have selected. This project focuses on plants that are tolerant of or adapted to serpentine soils and that are native to the Potrero Hill Neighborhood in San Francisco. This tool will be used to deveop the planting plan for the [Eco-Patch](https://www.greenbenefit.org/project-blog/2020/7/10/7h2nn73s0ae13hhxm61nwnjdnvkkls) project, which seeks to encourage people to use native plants with high habitat and biodiversity value. After using it to develop the Eco-Patch planting plan, this tool will be provided as part of an outreach effort as a way to further engage people with the Eco-Patch plants. The intention is that this tool, in coordination with physical Eco-Patch garden, will help people figure out which combinations of plants provide year-round interest in the form of flowers or green foliage. The beta version of this applicatipn can be found here.

## Data 

The application uses a plant data set from [Calscape](https://calscape.org/) that was downloaded as a spreadsheet and saved as a .csv file. Although this data set is a limit number of plants based on a small geographic region that are adapted to or tolerant of serpentines soils, because it works with Calscape data it has potential to be scaleable. In order to make the application print a color associated with the flower season, a column of RGB values corresponding to flower color was added to the spreadsheet prior to briging it into pandas.

## Libraries

* Pandas-
* Numpy-
* MatPlotLib-
* appJar-

## Functional Components

**Web_Application_Class**- simulates an interaction with a web application that allows users to login with a password (private variable), create a plant list, save their plant list, and create a visualization based on their plant list. This class can also accept new users. There is a function in this class that uses [appJar](http://appjar.info/) to create a Boolean widget checkbox for plant selection. The web application interface is text-based.

User_Class- stores user profiles and their list of plants for the web app class.

Data_Processing_Class- This class will read in a .csv file from a plant database and use pandas to manipulate the dataframe as needed to create the chart. The data has been pulled from a website, Calscape, which aggregates data about native plants. I am specifically interested in the columns with the current botanical name, the plant type (annual or perennial), evergreen/deciduous, flowers (which indicates flower color), and flowering season. Interpolation will be necessary to format the data from the calscape dataset into a usable form so that users can create a chart from it. For example, the data lists the season that the plants are flowering but does not list by month, and so I will need a function to convert the season to specific months for the chart. Also if the plant is listed as being deciduous for a particular season then I will need a function to convert that information to show an empty bar on the chart for the months in that season. If the plant is listed as evergreen then I will want the bar on the chart to show as green when the plant is not flowering and showing a flower color on the chart.

Chart_Class- this class creates a bar chart visualization showing when what plant is blooming or displaying green foliage from a list of plants. The planting visualization will list the plants on the y axis and the months on the x axis. For each month the plants have a color. The color is the flower color if the plant is blooming, otherwise green if it is evergreen, and blank if it is deciduous, dormant for certain months, or an annual that has died back for the year. The chart will use the third party library, MatPlotLib. 

## Summary

Future efforts include integrating the application into a website or a visual dashboard such as Plotly with an improved user interface. While the current application uses a limited color palette, eventually I would like to incorporate more diversity in the colors so that they more accurately represent the true flower and foliage color. for example, I would like to incorporate the nuances in the color of green foliage, as it can be used to further inform planting design decisions. 

In addition to being a tool to increase use of native plants and biodiversity, shifts in plant phenology can be used to track plant responses to climate change. It would be great if this application could also collect information based on individuals experiences with plants to get more fine grain data on specific regions and microclimates as well as to track shifts over time that could be the result of climate change.