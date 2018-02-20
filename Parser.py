import lxml
import requests
import csv
import time
from lxml import etree

#get the page's contents
routePage = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=ttc')
#form element tree
routeList = etree.fromstring(routePage.content)
#get all route numbers into an array
routes=[route.attrib['tag']for route in routeList]

#get current time in msec
msec = int(round(time.time() * 1000))

#open csv file
with open('log.csv', 'w', newline='') as f:
    #csv writer
    writer = csv.writer(f, delimiter = ',', quoting=csv.QUOTE_NONE)
    #write headings
    writer.writerow(['Route', 'Latitude', 'Longitude', 'Heading', 'Time'])
    for route in routes:
        #url for route
        url='http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r='+route+'&t='+str(msec)
        #get all locations of buses for route
        busPage = requests.get(url)
        #form element tree
        busList = etree.fromstring(busPage.content)
        #get time of request
        time = int(busList.find('lastTime').attrib['time'])
        for bus in busList.iter('vehicle'):
            #get actual time when bus is at position
            t=time-int(bus.attrib['secsSinceReport'])*1000
            #write to file
            writer.writerow([route, bus.attrib['lat'],bus.attrib['lon'],bus.attrib['heading'],t])