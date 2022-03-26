# Embedded file name: mod_customization_data.py
import csv
import types
import BigWorld
from CurrentVehicle import g_currentVehicle
from gui import SystemMessages
import items

class CustomizationData(object):
    def __init__(self, vehicles):
        # some tanks have an html icon for some reason, so we split on the closing html bracket
        self.vehiclesDict = {tank.intCD:tank.userName.split('>')[-1].decode('utf-8') for tank in vehicles.values()}

    def __print_tank_dict(self, dict):
        result = []
        for tank_id, count in dict.items():
            result.append('{}: {}'.format(self.vehiclesDict[tank_id], count))
        return '\n'.join(result)

    def __to_dict(self, obj):
        dict = {}
        dict['intCD'] = str(obj.intCD)
        dict['userName'] = str(obj.userName)
        dict['userType'] = str(obj.userType)
        dict['_inventoryCount'] = str(obj._inventoryCount)
        dict['_installedVehicles'] = self.__print_tank_dict(obj._installedVehicles)
        dict['_boundVehicles'] = self.__print_tank_dict(obj._boundVehicles)
        dict['texture'] = '"' + str(obj.texture) + '"'
        return dict

    def __get_customizations(self, items):
        for i in items:
            if i.userType in ['Camouflage', 'Inscription', 'Special', 'Decal', 'Emblem', 'Paint', 'Primary', 'Historical', 'Unique', 'Two-digit Number', 'Primary', 'Three-digit number', 'Effect', 'Rental']:
                yield i

    def write_csv(self, items):
        result = map(self.__to_dict, self.__get_customizations(items.values()))
        result = filter(lambda d: int(d['_inventoryCount']) != 0 or d['_installedVehicles'] != '' or d['_boundVehicles'] != '', result)
        result = sorted(result, key=lambda d: int(d['_inventoryCount']), reverse=True)
        result = sorted(result, key=lambda d: len(d['_installedVehicles']), reverse=True)
        result = sorted(result, key=lambda d: len(d['_boundVehicles']), reverse=True)
        with open('customization_elements.csv', 'w') as csv_file:
            headers = ['intCD', 'userName', 'userType', '_inventoryCount', '_installedVehicles', '_boundVehicles', 'texture']
            writer = csv.DictWriter(csv_file, fieldnames=headers, lineterminator='\n')
            writer.writeheader()
            writer.writerows(result)


#def dump_members(stream, obj):
#    stream.write(str(dir(obj)))
#
#def dump_style(stream, obj, level=0):
#    for name in dir(obj):
#        if name not in ['_boundVehicles', '_installedVehicles', 'icon', '_inventoryCount']:
#            continue
#        value = getattr(obj, name)
#        if not isinstance(value, types.InstanceType):
#            stream.write('  ' * level + '%s: %s\n' % (name, value))
#        else:
#            dump_style(stream, value, level + 1)
#
#def dump_values(stream, obj, level=0):
#    for name in dir(obj):
#        try:
#            value = getattr(obj, name)
#            if not isinstance(value, types.InstanceType):
#                stream.write('  ' * level + '%s: %s\n' % (name, value))
#            else:
#                dump_values(stream, value, level + 1)
#        except:
#            continue
#
#def write_style(items):
#    with open('__foo.txt', 'w') as file:
#        for obj in items.getStyles().values():
#            dump_style(file, obj)
#            file.write("\n\n\n")

def get_customization_data_callback():
    if g_currentVehicle.item is not None:
        #try:
        #    with open('__global1.txt', 'w') as file:
        #        dump_values(file, g_currentVehicle.itemsCache.items.getItemByCD(3847468))
        #except Exception, e:
        #    SystemMessages.pushMessage(str(e))
        #try:
        #    with open('__global2.txt', 'w') as file:
        #        dump_members(file, g_currentVehicle.itemsCache.items.getItemByCD(3847468))
        #except Exception, e:
        #    SystemMessages.pushMessage(str(e))

        obj = CustomizationData(g_currentVehicle.itemsCache.items.getVehicles())
        obj.write_csv(g_currentVehicle.itemsCache.items.getItems())
        SystemMessages.pushMessage('File written (customization_elements.csv).')
    else:
        BigWorld.callback(5, get_customization_data_callback)
    return


get_customization_data_callback()
