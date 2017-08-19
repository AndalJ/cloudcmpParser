import json
import pandas as pd
import csv

#####################################################################################
## @descr: save a json object to json file
## @params: jsonData ---- the json object of the data
##          fileFullName ---- the file name to save including the full path.
#####################################################################################
def dumpJson(jsonData, fileFullName):
    with open(fileFullName, 'w') as f:
        json.dump(jsonData, f, sort_keys=True, indent=4)

#####################################################################################
## @descr: load json object from json file
## @params: fileFullName ---- the file name to save including the full path.
## @return: data
#####################################################################################
def loadJson(fileFullName):
    json_data = open(fileFullName).read()
    data = json.loads(json_data)
    return data

#####################################################################################
## @descr: dump a list of json objects to a csv file
## @params: data  ---- list of json objects with the same keys
#           fileFullName ---- the file name to save including the full path.
#####################################################################################
def json2csv(data, fileFullName):
    df = pd.DataFrame(data)
    df.to_csv(fileFullName)

#####################################################################################
## @descr: read a csv file to json list
## @params: fileFullName ---- csv file name.
## @return: the list of csv rows as json dict
#####################################################################################
def csv2json(csvfilename):
    csv_rows = []
    with open(csvfilename) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
    return csv_rows

#####################################################################################
## @descr: read a csv file to json list
## @params: fileFullName ---- csv file name.
## @return: the list of csv rows as json dict, specify all fields as float
#####################################################################################
def csv2jsonfloat(csvfilename):
    csv_rows = []
    with open(csvfilename) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            # print(row)
            csv_rows.extend([{title[i]:float(row[title[i]]) for i in range(len(title))}])
    return csv_rows

## Replace the name for nodes by given values for drawing purpose
def replace_node_key(data, keyName, keyValuesToReplace):
    for node,ix in zip(data["nodes"], range(len(data["nodes"]))):
        if keyName in node.keys():
            curKeyVal = node[keyName]
            data["nodes"][ix]["org"+keyName] = curKeyVal
            if curKeyVal in keyValuesToReplace.keys():
                data["nodes"][ix][keyName] = keyValuesToReplace[curKeyVal]
            else:
                data["nodes"][ix][keyName] = ""
        else:
            data["nodes"][ix][keyName] = ""

    return data