import xml.etree.ElementTree as ET
tree = ET.parse('epcis_sample_zelthy.xml')
root = tree.getroot()
# print("root",root)
# print("tag",root.tag)
# print("attrib",root.attrib)
# print(root[0])
# childlevel_1=root[1]  #body
# childlevel_2 = childlevel_1[0] #eventlist
    
# for childlevel_3 in childlevel_2.getchildren(): #obj event
#     event_time = childlevel_3.find('epcList')
#     ev = event_time.find('epc')
#     print(ev)
#     if childlevel_3.tag == 'eventTime':
        # print(childlevel_3.text)
# print([elem.tag for elem in root.iter()])
# namespace_map = {'n1': 'http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader'}
# for r in root:
#     print("===",r.tag,r.attrib)
#     # print(r.find('n1:DocumentIdentification',namespaces=namespace_map))
#     for x in r.iter('n1:StandardBusinessDocumentHeader'):
#         print(x.attrib)
#         print("Sd")

# first_data = root.findall('EPCISHeader')
# print("first data",first_data)

import traceback
from datetime import datetime
from xml.etree.ElementTree import fromstring

def get_check_digit(epc):
        multipliers = [3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3]
        epc_comps = epc.split(":")[4].split(".")
        company_prefix = "0"+epc_comps[0]
        item_ref = epc_comps[1][1:]
        gtin_without_check = company_prefix+item_ref
        sum_number = 0
        i = 0
        for d in gtin_without_check:
            sum_number += int(d)*multipliers[i]
            i += 1
        if sum_number%10 == 0:
            check = str(0)
        else:
            check = str(10*(int(sum_number/10)+1)-sum_number)
        return check

def get_gtin_number(epc):
        epc_comps = epc.split(":")[4].split(".")
        company_prefix = "0"+epc_comps[0]
        item_ref = epc_comps[1][1:]
        serial_number = epc_comps[2]
        gtin = company_prefix + item_ref + get_check_digit(epc)
        return gtin

def get_sgtin_number(epc):
        epc_comps = epc.split(":")[4].split(".")
        serial_number = epc_comps[2]
        return get_gtin_number(epc) + serial_number

def get_serialization_details(root):
    try:
        # root = fromstring(file_string)
        events = root[1][0]
        result = []
        case_value = []
        for event in events.getchildren():
            case_info = []
            box_info = []
            if event.tag == 'AggregationEvent':
                parent_id_text = event.find('parentID').text
                parent_sscc = parent_id_text.split(":")[4].replace(".","")
                parent_info_added = False
                for e in event.find('childEPCs').getchildren():
                    epc_string = e.text
                    if 'sscc' in epc_string:
                        if not parent_info_added:
                            result.append({
                                'palette':parent_sscc,
                                'value':[]
                            })
                            parent_info_added = True
                        case_info.append({
                            'case': epc_string.split(":")[4].replace(".",""),
                            'value' : []
                        })
                        result[-1]['value'] = case_info
                
                    elif 'sgtin' in epc_string:
                        if not parent_info_added:
                            case_value.append({
                                'case':parent_sscc,
                                'value':[]
                            })
                            parent_info_added = True
                        box_info.append({
                            'sgtin':get_sgtin_number(epc_string),
                            'gtin':get_gtin_number(epc_string)
                        })
                        case_value[-1]['value'] = box_info

        case_value_dict = {cv['case']: cv['value'] for cv in case_value}
        for r in result:
            for v in r['value']:
                case = v['case']
                if case in case_value_dict:
                    v['value'] = case_value_dict[case]    

        return True, result

    except:
        return False, traceback.format_exc()


tree = ET.parse('epcis_sample_zelthy.xml')
root = tree.getroot()
is_valid, vial_data = get_serialization_details(root)
print(vial_data)
