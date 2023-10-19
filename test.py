import xml.etree.ElementTree as ET

a={'palette':"1234567890"}


epcis_document = ET.Element("EPCISDocument", xmlns="urn:epcglobal:epcis:xsd:1", schemaVersion="1.2")

epcis_header = ET.SubElement(epcis_document, "EPCISHeader")

epcis_body = ET.SubElement(epcis_document, "EPCISBody")

event_list = ET.SubElement(epcis_body, "EventList")


for x in a.values():
    
    object_event = ET.SubElement(event_list, "ObjectEvent")
    event_time = ET.SubElement(object_event, "eventTime")
    event_time.text = "2023-09-22T12:00:00Z"
    epc_list = ET.SubElement(object_event, "epcList")
    epc = ET.SubElement(epc_list, "epc")
    epc.text = x

# Create an ElementTree object
tree = ET.ElementTree(epcis_document)

# Save the XML to a file
tree.write("example.epcis.xml", encoding="utf-8", xml_declaration=True)

print("EPCIS XML file created.")



