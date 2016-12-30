import pprint
f = open('data1.txt')
workitem_types = ["Fundamental", "Experience", "Scenario"]
workitem_started = False
data = []
wi = {}
allowFirstAppend = False
for row in f:
    
    if row.startswith("Supporting:"):
        wi['supporting'] = row.split(',')[1:]

    # this needs to be at top, since we mark workitem_started later.
    if workitem_started:
        wi['description'] = row
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
        wi['type'] = row.split(' ')[0]
        wi['id'] = row.split(' ')[1]
        if len(row.split(' ')) > 2:
            pass

# EOF, append last wi
data.append(wi)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)