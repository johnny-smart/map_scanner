from lxml import etree
import os
import processor.config as config
import Switches


def main(map_loc):
    with open(map_loc, 'r', encoding='utf-8-sig') as xml_map_reader:
        xml_map = xml_map_reader.read()
        xml_map = etree(xml_map)

    for name in xml_map:
        for dev in name:
            print(dev)

    return


if __name__ == "__main__":
    main(config.XMLMAP)
