from lxml import etree
import json
import os
import config
import Switches


def main(map_loc, filter_option='Switch'):
    with open(map_loc, 'r', encoding='utf-8-sig') as xml_map_reader:
        xml_map = xml_map_reader.read()
        xml_map = etree.fromstring(xml_map)
    xml_map = filtration(xml_map, filter_option)

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


def result_uploading(result, directory='ignored'):
    if (os.path.isfile(directory+'/result_map.json')):
        os.remove(directory+'/result_map.json')

    json_file = open(directory+'/result_map.json', 'w+', encoding='utf-8')
    json_file.write(json.dumps(result))
    json_file.close()


if __name__ == "__main__":
    map_filter = main(config.XMLMAP)
    result_uploading(map_filter, config.JSONRESMAPF)
    sorter_map, len_map, without_config = Switches.result(map_filter)

    Switches.output(sorter_map, without_config, 'xml')
    print('done')
