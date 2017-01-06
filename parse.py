import pprint
import json
import re
import string
f = open('data1.txt')
workitem_types = ["Fundamental", "Experience", "Scenario", "Value Proposition"]
workitem_started = False
data = []
wi = {}
allowFirstAppend = False
for row in f:
    
    if row.startswith("Supporting"):
        value = row.strip().split(',')
        result = []
        for i in value:
            result.append(i.strip().split(' ')[-1])
        wi['supporting'] = result

    # this needs to be at top, since we mark workitem_started later.
    if workitem_started:
        wi['description'] = row.strip()
        workitem_started = False

    # check new workitem beggining
    workitem_starts = any([row.startswith(item) for item in workitem_types])
    if workitem_starts:

        workitem_started = True

        if allowFirstAppend:
            data.append(wi)
        else:
            allowFirstAppend = True

        wi = {}
        if row.startswith("Value Proposition"):
            if len(row.strip().split(' '))>2:
                wi['id'] = row.strip().split(' ')[2]
            else:
                wi['id'] = "None"
            wi['type'] =  " ".join((row.strip().split(' ')[0], row.strip().split(' ')[1]))
            if len(row.strip().split(' ')) > 3:
                if row.strip().split(' ')[3] == "--":
                    result = " ".join(map(str, row.strip().split(' ')[4:]))
                    wi['title'] = result
        else:
            wi['type'] = row.strip().split(' ')[0]
            wi['id'] = row.strip().split(' ')[1]
            if len(row.strip().split(' ')) > 2:
                wi['priority'] = row.strip().split(' ')[2]
                if len(row.strip().split(' ')) > 3:
                    if row.strip().split(' ')[3] == "--":
                        result = " ".join(map(str, row.strip().split(' ')[4:]))
                        wi['title'] = result

# EOF, append last wi
data.append(wi)
print json.dumps(data, ensure_ascii=False, encoding='utf8', indent=4)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(data)
# with open('output.txt', 'w') as outfile:
#     json.dump(data, outfile)
