# initialize variables to hold integers, floats, strings, lists
row = 0
ID_Count = -2
Weather = []
j = 0

# Import csv file
import csv
import datetime

# Set path of input csv file
file_name = "Resources/cities.csv"

# Open the csv file
with open(file_name, newline='') as csv_file:
    csvreader = csv.reader(csv_file)  # Read each line of Data as row

    for row in csvreader:
        Weather.append(row[3])  # Create Weather matrix with one city's weather data on each row
        ID_Count += 1  # Find number of cities
        print("<!-- Create HTML: ",row,"-->")
        print("   <tr>")
        print("      <td>", row[0], "</td>")  # HTML table row format for City_ID
        print("      <td>", row[1], "</td>")  # HTML table row format for City
        print("      <td>", row[2], "</td>")  # HTML table row format for Cloudiness
        print("      <td>", row[3], "</td>")  # HTML table row format for Country
        print("      <td>", row[4], "</td>")  # HTML table row format for Date datetime.datetime.utcnow()
        print("      <td>", row[5], "</td>")  # HTML table row format for Humidity
        print("      <td>", row[6], "</td>")  # HTML table row format for Latitude
        print("      <td>", row[7], "</td>")  # HTML table row format for Longitude
        print("      <td>", row[8], "</td>")  # HTML table row format for Max Temp
        print("      <td>", row[9], "</td>")  # HTML table row format for Wind Speed
        print("   </tr>")
    print('<--ID_Count:', ID_Count, "-->")

output_file = "Resources/weather_output.csv"
with open(output_file, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(Weather)
