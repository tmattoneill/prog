import urllib
import xml.etree.ElementTree as ET

x = 0

while True:
	url_to_scan = raw_input('Enter the URL: ')
	print 'Retrieving ', url_to_scan
	u_hand = urllib.urlopen(url_to_scan)
	xml_data = u_hand.read()
	print 'Retrieved', len(xml_data), 'bytes.'
	xml_tree = ET.fromstring(xml_data)
	counts = xml_tree.findall('.//count')
	print "Counts found: ", len(counts)
	for count in counts:
		x += int(count.text)
	print "Count sum: "	, x
