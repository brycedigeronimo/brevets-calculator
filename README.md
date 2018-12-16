# Project 6: Brevet Time Calculator Service

Author: Bryce Di Geronimo

Description: Reimplement the RUSA ACP controle time calculator using Docker, Flask, AJAX and Mongo db. Every time a user submits the form, the values are stored in the db. When the user presses display, the values are retrieved from the db and displayed on another page. This project also implements a RESTful API to return the open and close times in JSON and CSV format along with the requested top times.

Links to official brevet website and calculator:

https://rusa.org/pages/acp-brevet-control-times-calculator
https://rusa.org/octime_acp.html

The table below illustrates the Maximum speeds(open times) and the closing times(minimum times). If the control lands within the range, the time is control/(min or max) speed. The hour is rounded down to the nearest integer and the minutes are the remaining fraction without the hours * 60 rounded up. If the control lands on the end of the range such as 200, then it would be 200/15 or 200/34. Also, controls cannot be 20% over the brevet-distance. The 1000-1300 range would never be used for an ACP brevet. Units are in km/hr. 

Control location (km)   Minimum Speed (km/hr)   Maximum Speed (km/hr)
0-200                           15                      34
200-400                         15                      32
400-600                         15                      30 
600-1000                        11.428                  28
1000-1300                       13.333                  26


There are two hosts, 5000 for the calculator and 5001 for the API

To access the flask brevets calculator, go to http://localhost:5000. 

To access the API, to go http://localhost:5001 and use the services listed below:

    * http://localhost:5001/listAll returns all open and close times in the db
    * http://localhost:5001/listOpenOnly returns open times only
    * http://localhost:5001/listCloseOnly returns close times only
    * http://localhost:5001/listAll/csv returns all open and close times in CSV format
    * http://localhost:5001/listOpenOnly/csv returns open times only in CSV format
    * http://localhost:5001/listCloseOnly/csv returns close times only in CSV format
    * http://localhost:5001/listAll/json returns all open and close times in JSON format
    * http://localhost:5001/listOpenOnly/json returns open times only in JSON format
    * http://localhost:5001/listCloseOnly/json returns close times only in JSON format
    * To get top "x" open and close times, use a query parameter top.
    * http://localhost:5001/listOpenOnly/csv?top=x returns top x open times only (in ascending order) in CSV format 
    * http://localhost:5001listOpenOnly/json?top=x returns top x open times only (in ascending order) in JSON format
    * http://localhost:5001/listCloseOnly/csv?top=x returns top x close times only (in ascending order) in CSV format 
    * http://localhost:5001/listCloseOnly/json?top=x returns top x close times only (in ascending order) in JSON format
    * Examples of top 5 Open times listed below:
    * http://localhost:5001/listOpenOnly/csv?top=5 returns top 5 open times only (in ascending order) in CSV format 
    * http://localhost:5001listOpenOnly/json?top=5 returns top 5 open times only (in ascending order) in JSON format

Special cases:
    a) If control entered is a negative number, > 1000, or is 20% greater than brevet distance, an error page will be returned.
    b) If no input times are entered and the submit or display button is pressed, an error page will be returned telling the user to input values before submitting or dispalying.
    c) If control = brevet distance, then open and close times will be set to distance/max and distance/min respectively.
    d) Entering a negative value for a top value returns all values. 

Cases not accounted for:
    a) If the user enters a control that is less than the previous control, there is currently no error handling
    b) If the checkpoints are not entered in order, the top times will not be returned properly. 

To run application:
First, download Docker if you dont already have it. Then clone the repo and from the terminal, change directory into DockerRestAPI. Run the command "docker-compose up" and once everything has been built, go to your browser and go to http://localhost:5000 to submit times and to display them and go to http://localhost:5001 to access the API. 







