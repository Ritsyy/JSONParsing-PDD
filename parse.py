import pprint
import json
import re
import string
f = open('data1.txt')
workitem_types = ["Fundamental", "Experience", "Scenario", "Value Proposition"]
description_started = False
data = []
wi = {}
allowFirstAppend = False
for row in f:
    
    if row.strip().startswith("Supporting"):
        description_started = False
        result = []
        for item in row.strip().split(','):
            for i in item.split():
                if i[0].isdigit():
                    result.append(i)
        wi['supporting'] = result

    # check new workitem beggining
    workitem_starts = any([row.startswith(item) for item in workitem_types])
    if workitem_starts:

        description_started = True

        if allowFirstAppend:
            data.append(wi)
        else:
            allowFirstAppend = True

        wi = {}
        wi['description'] = ''
        if row.startswith("Value Proposition"):
            if len(row.strip().split(' '))>2:
                wi['id'] = row.strip().split(' ')[2]
            else:
                wi['id'] = "None"
            wi['type'] =  " ".join((row.strip().split(' ')[0], row.strip().split(' ')[1]))
            if len(row.strip().split(' ')) > 3:
                if row.strip().split(' ')[3] == "--" or row.strip().split(' ')[3] == "-":
                    result = " ".join(map(str, row.strip().split(' ')[4:]))
                    wi['title'] = result
        else:
            wi['type'] = row.strip().split(' ')[0]
            wi['id'] = row.strip().split(' ')[1]
            if len(row.strip().split(' ')) > 2:
                if row.strip().split(' ')[2] == "--":
                    result = " ".join(map(str, row.strip().split(' ')[3:]))
                    wi['title'] = result
                else:
                    wi['priority'] = row.strip().split(' ')[2]
                if len(row.strip().split(' ')) > 3:
                    if row.strip().split(' ')[3] == "--" or  row.strip().split(' ')[3] == "-":
                        result = " ".join(map(str, row.strip().split(' ')[4:]))
                        wi['title'] = result
        
    if description_started and workitem_starts == False:
        wi['description'] = wi['description'] + row.strip()


# EOF, append last wi
data.append(wi)
print json.dumps(data, ensure_ascii=False, encoding='utf8', indent=4)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(data)
# with open('output.txt', 'w') as outfile:
#     json.dump(data, outfile)
