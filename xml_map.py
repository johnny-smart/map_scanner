from lxml import etree
import json
import os
import config
import Switches
from operator import itemgetter

def main(map_loc, filter_option='Switch'):
    with open(map_loc, 'r', encoding='utf-8-sig') as xml_map_reader:
        xml_map = xml_map_reader.read()
        xml_map = etree.fromstring(xml_map)
    xml_map = filtration(xml_map, filter_option)
    result_uploading(xml_map,'filtred_smart.json')
    return xml_map


def filtration(xml_map, option):
    filtred_map = {}
    for name in xml_map:
        if name.tag == 'Devices':
            for dev in name:
                if {**dev.attrib}.get('type-id') == option:
                    filtred_map.update({dev.attrib['id']: {**dev.attrib}})
                    description = dev.getchildren()
                    filtred_map[dev.attrib['id']].update({
                        'description': description[0].text
                        })
    return filtred_map


def scan_map_names(filtred_map):
    scan_failed = []
    for record in filtred_map.values():
        if not record['name'].split()[-1][0].isdigit():
            scan_failed.append({'name':record['name'], 'address': record['address']})
    scan_failed = sorted(scan_failed, key=itemgetter('address'))
    return scan_failed


def result_uploading(result, fname = 'result_map.json', directory=config.DIR):
    if (os.path.isfile(directory + '/' + fname)):
        os.remove(directory + '/' + fname)

    json_file = open(directory + '/' + fname, 'w+', encoding='utf-8')
    json_file.write(json.dumps(result))
    json_file.close()
    print(fname)


if __name__ == "__main__":
    map_filter = main(config.XMLMAP)

    scan_names = scan_map_names(map_filter)

    if config.JSONRESMAPF:
        result_uploading(map_filter, config.JSONRESMAPF)
    else:
        result_uploading(map_filter)
    sorter_map, len_map, without_config = Switches.result(map_filter)

    result_uploading(scan_names,'name_epic_fail.json')

    Switches.output(sorter_map, without_config, config.DIR)
    print('done')
