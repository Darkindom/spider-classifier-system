# coding=utf-8
import json
import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

path_file = os.path.abspath(sys.argv[0])
path_file = os.path.dirname(path_file) + '/'
path_source = path_file + 'spider_json/'
path_destination = path_file + 'files_toES/'
kinds = 8

print path_file
print path_source
print path_destination

for i in xrange(1, kinds+1):
    print i
    file_source = open(path_source + 'data_' + str(i) + '.json', "r")
    file_destination = open(path_destination + 'data_' + str(i) + '.json', "w")

    data_source = json.load(file_source)
    file_source.close

    data_list = data_source['data']
    data_type = data_list[0]['fields']
    data_id = 1
    data_destination = []

    for data in data_list:
        index = { "index": {"_index": "info", "_type": data_type, "_id": data_id}}
        # data_destination.append(index)
        json.dump(index, file_destination, sort_keys = True)
        # data_destination.append(data)
        # json.dump('', file_destination, sort_keys = True)
        json.dump(data, file_destination, sort_keys = True)
        data_id += 1

    # json.dump(data_destination, file_destination, sort_keys = True)

print 'toES end'
