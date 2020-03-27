import json
import os
import config

vendors = {'D-Link': ['DES', 'DGS'], 'Eltex': ['MES'], 'Zyxel': ['IES'], 'Other_vendor': [], 'None_vendor': [], }
# vendors.update({'Cisco': ['WS-']})


def main():
    map_group = {}

    map_dev = open(config.DIR + 'result_map.json', 'r', encoding='utf-8-sig')
    map_dev_all = json.load(map_dev)
    map_group = filter_by_group_type(map_dev_all, 'Switch')

    sorted_group, result_lenght, without_config = result(map_group, 'key')

    return sorted_group, result_lenght, without_config


def result(map_group, configuration='default'):
    result_lenght = len(map_group)
    without_conf = {}
    if configuration == 'key':
        map_group = rename(map_group)

    sorted_group = sort_group(map_group)

    for lists in vendors:
        if not(lists in ['Other_vendor', 'None_vendor']):
            without_conf.update(non_config(sorted_group[lists], lists))

    for lists in vendors:
        if not(lists in ['Other_vendor', 'None_vendor']):
            sorted_group.update(untwin(sorted_group.pop(lists), lists))

        else:
            sorted_group.update(unlist(sorted_group.pop(lists), lists))

    return sorted_group, result_lenght, without_conf


def rename(dictionary):
    for item in dictionary:
        for name in dictionary[item]:
            dictionary[item][name.lower()] = dictionary[item].pop(name)
    return dictionary


def filter_by_group_type(map_all, group):

    map_group = {}

    for dev_name, dev in map_all.items():
        if (not dev_name == 'Apperance') and dev.get('type-id') == group:
            map_group.update({dev_name: dev})

    return map_group


def unlist(model_list, name_vendor):
    result = {}
    count = 0
    for address in model_list:
        count += 1
        result.update({str(count): address})
    return {name_vendor: result}


def non_config(model_list, name_vendor):
    without_config = {}

    for dev in model_list:
        if config.DEVICE_TYPES.get(name_vendor):
            if dev['description'] not in config.DEVICE_TYPES[name_vendor]:
                if not without_config.get(dev['description']):
                    without_config.update({dev['description']:[]})
                without_config[dev['description']].append(dev['address'])
        else:
            without_config.update({name_vendor:dev['address']+' Вендор не найден в файле config'})
    return {name_vendor:without_config}


def untwin(model_list, name_vendor):
    result = {}
    lenght = len(model_list)

    for model in model_list:
        if model['description'].upper() not in result:
            result.update({model['description'].upper(): 1})
        else:
            result[model['description'].upper()] += 1

    result.update({'total_count': lenght})

    return {name_vendor: result}


def sort_group(map_group):
    map_group_result = {}
    for vendor in vendors:
        map_group_result.update({vendor: []})

    for dev_name in map_group:
        element = map_group[dev_name]
        if element.get('description'):
            element['description'] = element['description'].split('\n')[0]
            map_group_result = description_in_vendors(element, map_group_result)
        else:
            map_group_result['None_vendor'].append(element)

    return map_group_result


def description_in_vendors(element, map_group):

    flag = False

    if isinstance(element['name'], list):
        element['name'] = '-'.join(element['name'])

    for vendor in vendors:
        if element['description'][0:3:1] in vendors[vendor]:
            element['description'] = element['description'].split(' ')[0]
            map_group[vendor].append(element)
            flag = True

    if flag is False:
        map_group['Other_vendor'].append(element)

    return map_group


def test_count(map_dev, count):
    flag = None
    result_count = 0
    for vend in vendors:
        if map_dev[vend].get('total_count') != None:
            result_count += map_dev[vend]['total_count']
        else:
            result_count += len(map_dev[vend])

    if count == result_count:
        flag = True
    else:
        flag = False

    return flag, result_count, count


def to_json(object_python, fname):
    json_file = open(fname, 'w', encoding='utf-8-sig')
    json_file.write(json.dumps(object_python, indent=4, sort_keys=True))
    print(fname)
    json_file.close()


def output(group, without_conf, directory=config.DIR):
    if (os.path.isfile(directory+'error_vendors.json')):
            os.remove(directory+'error_vendors.json')

    if (os.path.isfile(directory+'without_config.json')):
        os.remove(directory+'without_config.json')

    to_json((group['Other_vendor'], group['None_vendor']), directory+'error_vendors.json')
    to_json(group, directory+'models.json')
    to_json(without_conf, directory+'without_config.json')



if __name__ == "__main__":
    group, start_lenght_group, without_conf = main()

    print(test_count(group, start_lenght_group))

    output(group, without_conf)


    print('done')

