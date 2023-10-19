import xml.etree.ElementTree as ET

input_data=[{
	'palette': '46022100000342649',
	'value': [{
		'case': '46022100000342647',
		'value': [{
			'sgtin': '088061550178169999999810000',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810001',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810002',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810003',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810004',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810005',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810006',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810007',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810008',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810009',
			'gtin': '08806155017816'
		}]
	}, {
		'case': '46022100000342648',
		'value': [{
			'sgtin': '088061550178169999999810010',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810011',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810012',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810013',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810014',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810015',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810016',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810017',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810018',
			'gtin': '08806155017816'
		}, {
			'sgtin': '088061550178169999999810019',
			'gtin': '08806155017816'
		}]
	}]
}]

epcis_document = ET.Element("EPCISDocument", xmlns="urn:epcglobal:epcis:xsd:1", schemaVersion="1.1")
epcis_header = ET.SubElement(epcis_document, "EPCISHeader")
epcis_body = ET.SubElement(epcis_document, "EPCISBody")
event_list = ET.SubElement(epcis_body, "EventList")

def create_epc_element(element,num,type):
	epc = ET.SubElement(element, "epc")
	if type == 'sgtin':
		epc.text = 'urn:epc:id:sgtin:' + num[1:8]+ '.' + '0' + num[8:13] + '.' + num[14:] 
	elif type == 'sscc':
		epc.text = 'urn:epc:id:sscc:' + num[:7] + '.' + num[7:]


def create_object_event(data, type):
	object_event = ET.SubElement(event_list, "ObjectEvent")
	epc_list = ET.SubElement(object_event, "epcList")
	for x in data:
		create_epc_element(epc_list, x,type)

def create_aggregation_event(data, type):
	for key,values in data.items():
		aggregation_event = ET.SubElement(event_list, "AggregationEvent")
		parent_id = ET.SubElement(aggregation_event, "parentID")
		parent_id.text =  'urn:epc:id:sscc:' + key[:7] + '.' + key[7:]
		child_epcs = ET.SubElement(aggregation_event, "childEPCs")
		for value in values:
			if type == 'sgtin':
				value = value['sgtin']
			create_epc_element(child_epcs,value,type)

palettes=[]
cases = []
palettes_n_cases = {}
cases_n_boxes = {}
boxes = []

for data in input_data:
    palettes.append(data['palette'])
    for case_data in data['value']:
        cases.append(case_data['case'])
        if data['palette'] in palettes_n_cases:
            palettes_n_cases[data['palette']].append(case_data['case'])
        else:
            palettes_n_cases[data['palette']] = [case_data['case']]
		
        cases_n_boxes[case_data['case']] = case_data['value']
        boxes.extend([x['sgtin'] for x in case_data['value']])

create_object_event(boxes, 'sgtin')
create_object_event(palettes, 'sscc')
create_object_event(palettes+cases, 'sscc')
create_aggregation_event(palettes_n_cases, 'sscc')
create_aggregation_event(cases_n_boxes, 'sgtin')

tree = ET.ElementTree(epcis_document)
tree.write("epcis4.xml", encoding="utf-8", xml_declaration=True)

print("EPCIS XML file created.")
