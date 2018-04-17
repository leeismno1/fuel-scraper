import requests
from lxml import etree as ET
import collections, itertools
from pprint import pprint

# Returns a list of URLs based on the variables for fueld_types, regions and day.
def gen_fuel(fuel_types, regions, day):

    fuel_watch_urls_list = [
        'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={}&Region={}&Day={}'.format(*i)
        for i in itertools.product(fuel_types, regions, day)
    ]
    return fuel_watch_urls_list

# for each in listed_fuel_watch_urls:
#    print(each)

# Uses the URLs created with function def gen_fuel and from the XML grabs the data and adds it to a dictionary, leaving a list of dictionaries with all data.
def get_fuel_data(listed_fuel_watch_urls):
    for item in listed_fuel_watch_urls:
        item = requests.get(item)

        dataContent = ET.fromstring(item.content)

        allItems = dataContent.findall('.//item')
        list_of_dicts = []
        for info in allItems:

            price = info.find('price').text
            address = info.find('address').text
            location = info.find('location').text
            name = info.find('trading-name').text

            data_dict =  {
                'price': price,
                'address': address,
                'location': location,
                'name': name,
            }
            list_of_dicts.append(data_dict)

        data1 = sorted(list_of_dicts, key=lambda k: k ['price'])
        return list_of_dicts


# These variables provide the information to what fuel types, area and day that the gen_fuel function uses to create the required URLS.
fuel_types = [1, 2, 6]
regions = [25, 27]
day = ['today', 'tomorrow']

# The out come of function gen_fuel and the variables for fuel type, region and days.
listed_fuel_watch_urls = gen_fuel(fuel_types, regions, day)

# This variable is the data provided from the list of dictonaries in funtion get_fuel_data and passes the list of URLs.
fuel_data = get_fuel_data(listed_fuel_watch_urls)

# pprint(fuel_data, indent=4)

# print(fuel_data)

# converts the list of dictionaries a string.
fuel_data_string = str(fuel_data)

# Formats the html.
fuel_data_html = "<html><title>Fuel Report</title><body>" + fuel_data_string + "</body></html>"

# Opens and creates a file named fuel_report.html with write access.
fuel_file = open('fuel_report.html', 'w')

# Writes the the data from fuel_data_html into the fuel_report.html file.
fuel_file.write(fuel_data_html)

# Closes fuel_report.html.
fuel_file.close

