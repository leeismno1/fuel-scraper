import requests
from lxml import etree as ET
import collections, itertools
from pprint import pprint

def gen_fuel(fuel_types, regions, day):

    fuel_watch_urls_list = [
        'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product={}&Region={}&Day={}'.format(*i)
        for i in itertools.product(fuel_types, regions, day)
    ]
    return fuel_watch_urls_list

# for each in listed_fuel_watch_urls:
#    print(each)


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



fuel_types = [1, 2, 6]
regions = [25, 27]
day = ['today', 'tomorrow']

listed_fuel_watch_urls = gen_fuel(fuel_types, regions, day)

fuel_data = get_fuel_data(listed_fuel_watch_urls)

pprint(fuel_data, indent=4)


"""


def gen_fuel(fuel_types):
    for each in fuel_types:
        result = ('http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=' +str(each)+ '&Region=25&Day=today')
        print(result)

fuel_types = [1, 2, 6]
gen_fuel(fuel_types)

def gen_days(days):
    for each_day in days:
        result = ('http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=6&Region=25&Day='+each_day)
        print(result)

days = ['today', 'tomorrow']
gen_days(days)


def gen_region(region):
    for location in region:
        result = ('http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=6&Region='+str(location)+'&Day=today')
        print(result)

region = [25, 27]
gen_region(region)

def get_prices(day):
    data = requests.get('http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=6&Region=25&Day=')
    dataContent = ET.fromstring(data.content)



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

    data1 = sorted(list_of_dicts, key=lambda k: k ['price'])"""

